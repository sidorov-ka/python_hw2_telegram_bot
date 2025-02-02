from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from services.database import get_user_data, save_user_data
from services.food_api import get_calories
from utils.states import FoodStates, WaterStates, WorkoutStates
import logging

router = Router()

# Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# ✅ Логирование воды через FSM
@router.message(Command("log_water"))
async def log_water_start(message: Message, state: FSMContext):
    await message.answer("💧 Введите количество выпитой воды (мл):")
    await state.set_state(WaterStates.quantity)


@router.message(WaterStates.quantity)
async def log_water_finish(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    if not user_data:
        await message.answer("❌ Сначала настройте профиль с помощью /set_profile.")
        await state.clear()
        return

    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError

        user_data["logged_water"] = user_data.get("logged_water", 0) + amount
        save_user_data(user_id, user_data)
        await message.answer(f"✅ Записано: {amount} мл воды.")
    except ValueError:
        await message.answer("❗ Введите корректное число (мл).")

    await state.clear()


# ✅ Логирование еды через FSM
@router.message(Command("log_food"))
async def log_food_start(message: Message, state: FSMContext):
    await message.answer("🍽 Введите название продукта:")
    await state.set_state(FoodStates.name)


@router.message(FoodStates.name)
async def log_food_name(message: Message, state: FSMContext):
    food_name = message.text.strip()

    try:
        calories = get_calories(food_name)
        if not calories:
            await message.answer("⚠ Продукт не найден. Попробуйте другой запрос.")
            await state.clear()
            return

        await state.update_data(food_name=food_name, calories=calories)
        await message.answer(f"{food_name} содержит {calories} ккал на 100 г. Сколько граммов вы съели?")
        await state.set_state(FoodStates.quantity)
    except Exception as e:
        logging.error(f"Ошибка Nutritionix API: {e}")
        await message.answer("⚠ Ошибка при получении данных. Попробуйте позже.")
        await state.clear()


@router.message(FoodStates.quantity)
async def log_food_quantity(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    if not user_data:
        await message.answer("❌ Сначала настройте профиль с помощью /set_profile.")
        await state.clear()
        return

    try:
        quantity = float(message.text)
        if quantity <= 0:
            raise ValueError

        data = await state.get_data()
        food_name = data["food_name"]
        calories_per_100g = data["calories"]
        total_calories = (calories_per_100g / 100) * quantity

        user_data["logged_calories"] = user_data.get("logged_calories", 0) + total_calories
        save_user_data(user_id, user_data)

        await message.answer(f"✅ Добавлено: {food_name}, {quantity} г — {total_calories:.2f} ккал.")
    except ValueError:
        await message.answer("❗ Введите корректное число (граммы).")

    await state.clear()


# ✅ Логирование тренировок через FSM
@router.message(Command("log_workout"))
async def log_workout_start(message: Message, state: FSMContext):
    await message.answer("🏋 Введите тип тренировки:")
    await state.set_state(WorkoutStates.type)


@router.message(WorkoutStates.type)
async def log_workout_type(message: Message, state: FSMContext):
    workout_type = message.text.strip()
    await state.update_data(workout_type=workout_type)
    await message.answer(f"⌛ Введите длительность тренировки (в минутах):")
    await state.set_state(WorkoutStates.duration)

# Таблица MET
MET_VALUES = {
    "running": 9.8,
    "cycling": 7.5,
    "swimming": 8.0,
    "yoga": 3.0,
    "weightlifting": 6.0,
}

@router.message(WorkoutStates.duration)
async def log_workout_duration(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    if not user_data or "weight" not in user_data:
        await message.answer("❌ Сначала настройте профиль с помощью /set_profile.")
        await state.clear()
        return

    try:
        duration = int(message.text)
        if duration <= 0:
            raise ValueError

        data = await state.get_data()
        workout_type = data["workout_type"].lower()

        if workout_type not in MET_VALUES:
            available_workouts = ", ".join(MET_VALUES.keys())
            await message.answer(f"⚠ Вид активности не найден. Доступные варианты: {available_workouts}")
            await state.clear()
            return

        met = MET_VALUES[workout_type]
        weight = user_data["weight"]
        burned_calories = met * weight * (duration / 60)  # Перевод минут в часы

        user_data["burned_calories"] = user_data.get("burned_calories", 0) + burned_calories
        save_user_data(user_id, user_data)

        await message.answer(f"✅ {workout_type} ({duration} минут) — {burned_calories:.2f} ккал сожжено.")
    except ValueError:
        await message.answer("❗ Введите корректное число (минуты).")

    await state.clear()
