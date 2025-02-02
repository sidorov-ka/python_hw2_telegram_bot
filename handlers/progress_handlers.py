from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.database import get_user_data
from services.calculations import calculate_water_norm, calculate_calorie_norm
from services.weather_api import fetch_temperature
from utils.helpers import format_progress_text

router = Router()

# Обработчик команды /check_progress
@router.message(Command("check_progress"))
async def check_progress(message: Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    if not user_data:
        await message.answer("❌ У вас пока нет профиля. Используйте /set_profile для настройки.")
        return

    # Получаем температуру в городе пользователя
    city = user_data.get("city", "")
    _, temperature = fetch_temperature(city) if city else (None, None)

    # Рассчитываем нормы с учётом температуры
    water_norm = calculate_water_norm(user_data, temperature)
    calorie_norm = calculate_calorie_norm(user_data)

    # Получаем данные из профиля (если нет — подставляем 0)
    logged_water = user_data.get("logged_water", 0)
    logged_calories = user_data.get("logged_calories", 0)
    burned_calories = user_data.get("burned_calories", 0)

    # Формируем текст прогресса
    progress_text = format_progress_text(water_norm, logged_water, calorie_norm, logged_calories, burned_calories)
    await message.answer(progress_text)
