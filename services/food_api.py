import requests
from utils.config import NUTRITIONIX_APP_ID, NUTRITIONIX_API_KEY

def get_calories(food_name: str) -> float:
    """
    Получает калорийность продукта через Nutritionix API.
    :param food_name: Название продукта на английском.
    :return: Калорийность на 100 грамм.
    """
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "query": food_name,
        "locale": "en_US"
    }

    # Отправка запроса
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        food_data = result["foods"][0]
        calories = food_data["nf_calories"]
        serving_weight_grams = food_data["serving_weight_grams"]

        # Рассчитываем калорийность на 100 грамм
        calories_per_100g = (calories / serving_weight_grams) * 100
        return round(calories_per_100g, 2)
    else:
        raise Exception(f"Ошибка: {response.status_code}, {response.text}")
