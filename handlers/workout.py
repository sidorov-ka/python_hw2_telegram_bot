from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.filters import Command
from states import WorkoutStates
from database import update_user, get_user  # Добавляем работу с БД


async def log_workout(message: types.Message, state: FSMContext):
    await message.answer("Введите тип тренировки (например, бег, плавание и т.д.):")
    await state.set_state(WorkoutStates.workout_type)


async def log_workout_duration(message: types.Message, state: FSMContext):
    await state.update_data(workout_type=message.text)
    await message.answer("Сколько минут длилась тренировка?")
    await state.set_state(WorkoutStates.workout_duration)


async def log_workout_final(message: types.Message, state: FSMContext):
    try:
        duration = int(message.text)
        data = await state.get_data()
        workout_type = data["workout_type"]
        calories_burned = duration * 10  # Примерный расчет калорий

        user_id = message.from_user.id
        user_data = await get_user(user_id)

        if user_data:
            new_burned_calories = user_data["burned_calories"] + calories_burned
            await update_user(user_id, "burned_calories", new_burned_calories)

        await message.answer(f"Вы сделали {workout_type} на {duration} минут. Сожжено: {calories_burned} ккал.")
        await state.clear()

    except ValueError:
        await message.answer("Введите корректное число минут.")


def register_workout_handlers(dp: Dispatcher):
    dp.message.register(log_workout, Command("log_workout"))
    dp.message.register(log_workout_duration, state=WorkoutStates.workout_type)
    dp.message.register(log_workout_final, state=WorkoutStates.workout_duration)
