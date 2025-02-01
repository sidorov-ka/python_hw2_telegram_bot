import os
from dotenv import load_dotenv

# Загружаем переменные из .env, если он существует
load_dotenv()

# Получаем переменные окружения
API_TOKEN = os.getenv("API_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Проверяем, загружены ли ключевые переменные
if not API_TOKEN:
    raise ValueError("Ошибка: переменная API_TOKEN не задана в .env!")

if not WEATHER_API_KEY:
    raise ValueError("Ошибка: переменная WEATHER_API_KEY не задана в .env!")
