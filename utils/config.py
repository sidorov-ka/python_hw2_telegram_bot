import os
from dotenv import load_dotenv

# Загружаем переменные из .env, если он существует
load_dotenv()

# Получаем переменные окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")

# Проверяем, загружены ли ключевые переменные
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Ошибка: переменная API_TOKEN не задана в .env!")

if not WEATHER_API_KEY:
    raise ValueError("Ошибка: переменная OPENWEATHER_API_KEY не задана в .env!")

if not NUTRITIONIX_APP_ID:
    raise ValueError("Ошибка: переменная NUTRITIONIX_APP_ID не задана в .env!")

if not NUTRITIONIX_API_KEY:
    raise ValueError("Ошибка: переменная NUTRITIONIX_API_KEY не задана в .env!")