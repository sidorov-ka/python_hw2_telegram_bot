import requests
from utils.config import WEATHER_API_KEY

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_temperature(city: str) -> tuple:
    """
    Получает температуру.
    :param city: Название города.
    :return: Кортеж (город, температура) или (город, None) в случае ошибки.
    """
    url = f"{BASE_URL}?q={city}&units=metric&APPID={WEATHER_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, есть ли ошибки в ответе

        data = response.json()

        # Извлекаем нужные данные
        if 'main' in data and 'temp' in data['main']:
            temperature = data['main']['temp']
            return city, temperature
        else:
            return city, None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return city, None