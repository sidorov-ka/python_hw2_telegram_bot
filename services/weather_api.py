import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> dict:
    """Получаем погоду для заданного города"""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",  # Температура в градусах Цельсия
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()  # Возвращаем JSON с данными о погоде
    else:
        return {"error": "Unable to fetch weather data"}

# Пример использования:
# weather_data = get_weather("Moscow")