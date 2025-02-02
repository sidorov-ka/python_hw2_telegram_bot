from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from services.database import save_user_data
from services.weather_api import fetch_temperature
from utils.states import ProfileStates
import logging

router = Router()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def is_valid_number(text: str) -> bool:
    """Проверяет, является ли введённое значение числом."""
    try:
        float(text)
        return True
    except ValueError:
        return False


@router.message(Command("set_profile"))
async def set_profile(message: Message, state: FSMContext):
    await message.answer("📌 Давайте настроим ваш профиль.\nВведите ваш вес (в кг):")
    await state.set_state(ProfileStates.weight)


@router.message(ProfileStates.weight, F.text)
async def process_weight(message: Message, state: FSMContext):
    if not is_valid_number(message.text):
        await message.answer("⚠ Введите число (например, 70).")
        return

    await state.update_data(weight=float(message.text))
    await message.answer("✅ Вес сохранён! Теперь введите ваш рост (в см):")
    await state.set_state(ProfileStates.height)


@router.message(ProfileStates.height, F.text)
async def process_height(message: Message, state: FSMContext):
    if not is_valid_number(message.text):
        await message.answer("⚠ Введите число (например, 175).")
        return

    await state.update_data(height=float(message.text))
    await message.answer("✅ Рост сохранён! Теперь введите ваш возраст:")
    await state.set_state(ProfileStates.age)


@router.message(ProfileStates.age, F.text)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠ Введите целое число (например, 25).")
        return

    await state.update_data(age=int(message.text))
    await message.answer("✅ Возраст сохранён! Сколько минут активности у вас в день?")
    await state.set_state(ProfileStates.activity)


@router.message(ProfileStates.activity, F.text)
async def process_activity(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠ Введите целое число (например, 60).")
        return

    await state.update_data(activity=int(message.text))
    await message.answer("✅ Активность сохранена! В каком городе вы находитесь?")
    await state.set_state(ProfileStates.city)


@router.message(ProfileStates.city, F.text)
async def process_city(message: Message, state: FSMContext):
    city = message.text
    city, temperature = fetch_temperature(city)

    if temperature is None:
        await message.answer("⚠ Не удалось получить температуру для этого города. "
                             "Убедитесь, что название на английском языке (например, Moscow).")
        return

    user_data = await state.get_data()
    user_data.update({"city": city, "temperature": temperature})

    save_user_data(message.from_user.id, user_data)

    await message.answer(
        f"🎉 Профиль сохранён!\n"
        f"🔹 Вес: {user_data['weight']} кг\n"
        f"🔹 Рост: {user_data['height']} см\n"
        f"🔹 Возраст: {user_data['age']} лет\n"
        f"🔹 Активность: {user_data['activity']} мин/день\n"
        f"🌍 Город: {user_data['city']}\n"
        f"🌡 Текущая температура: {user_data['temperature']}°C\n\n"
        "Теперь вы можете логировать воду, еду и тренировки."
    )

    await state.clear()
