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

# ✅ Проверка, что введённое сообщение - число
def is_valid_number(text: str) -> bool:
    try:
        float(text)
        return True
    except ValueError:
        return False

# ✅ Начало настройки профиля
@router.message(Command("set_profile"))
async def set_profile(message: Message, state: FSMContext):
    await message.answer("📌 Давайте настроим ваш профиль.\nВведите ваш вес (в кг):")
    await state.set_state(ProfileStates.weight)

# ✅ Обработчик ввода веса
@router.message(ProfileStates.weight, F.text)
async def process_weight(message: Message, state: FSMContext):
    if not is_valid_number(message.text):
        await message.answer("⚠ Введите число (например, 70).")
        return

    await state.update_data(weight=float(message.text))
    await message.answer("✅ Вес сохранён! Теперь введите ваш рост (в см):")
    await state.set_state(ProfileStates.height)

# ✅ Обработчик ввода роста
@router.message(ProfileStates.height, F.text)
async def process_height(message: Message, state: FSMContext):
    if not is_valid_number(message.text):
        await message.answer("⚠ Введите число (например, 175).")
        return

    await state.update_data(height=float(message.text))
    await message.answer("✅ Рост сохранён! Теперь введите ваш возраст:")
    await state.set_state(ProfileStates.age)

# ✅ Обработчик ввода возраста
@router.message(ProfileStates.age, F.text)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠ Введите целое число (например, 25).")
        return

    await state.update_data(age=int(message.text))
    await message.answer("✅ Возраст сохранён! Сколько минут активности у вас в день?")
    await state.set_state(ProfileStates.activity)

# ✅ Обработчик ввода активности
@router.message(ProfileStates.activity, F.text)
async def process_activity(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠ Введите целое число (например, 60).")
        return

    await state.update_data(activity=int(message.text))
    await message.answer("✅ Активность сохранена! В каком городе вы находитесь?")
    await state.set_state(ProfileStates.city)

# ✅ Обработчик ввода города с проверкой температуры
@router.message(ProfileStates.city, F.text)
async def process_city(message: Message, state: FSMContext):
    city = message.text
    city, temperature = fetch_temperature(city)

    if temperature is None:
        await message.answer("⚠ Не удалось получить температуру для этого города. Попробуйте другой город.")
        return

    await state.update_data(city=city, temperature=temperature)

    data = await state.get_data()
    await message.answer(
        f"🎯 Проверьте введённые данные:\n"
        f"🔹 Вес: {data['weight']} кг\n"
        f"🔹 Рост: {data['height']} см\n"
        f"🔹 Возраст: {data['age']} лет\n"
        f"🔹 Активность: {data['activity']} мин/день\n"
        f"🌍 Город: {data['city']}\n"
        f"🌡 Текущая температура: {data['temperature']}°C\n\n"
        f"✅ Всё верно? Напишите 'Да' для сохранения или 'Нет' для отмены."
    )

    await state.set_state(ProfileStates.confirm)

# ✅ Подтверждение профиля
@router.message(ProfileStates.confirm, F.text)
async def process_confirmation(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        user_data = await state.get_data()
        save_user_data(message.from_user.id, user_data)

        await message.answer("🎉 Профиль успешно сохранён! 🎯\n\n"
                             f"🌍 Город: {user_data['city']}\n"
                             f"🌡 Текущая температура: {user_data['temperature']}°C\n"
                             "Теперь вы можете логировать воду, еду и тренировки.")
        await state.clear()
    elif message.text.lower() == "нет":
        await message.answer("❌ Настройка отменена. Вы можете повторить команду /set_profile.")
        await state.clear()
    else:
        await message.answer("⚠ Пожалуйста, введите 'Да' или 'Нет'.")
