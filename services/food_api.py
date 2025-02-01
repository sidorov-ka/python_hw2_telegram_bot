import requests

BASE_URL = "https://world.openfoodfacts.org/api/v0/product/"

def get_food_data(product_name: str) -> dict:
    """Получаем данные о продукте через OpenFoodFacts API"""
    url = f"{BASE_URL}{product_name}.json"
    response = requests.get(url)

    if response.status_code == 200:
        product_data = response.json()
        if product_data['status'] == 1:
            return product_data['product']
        else:
            return {"error": "Product not found"}
    else:
        return {"error": "Unable to fetch product data"}

# Пример использования:
# food_data = get_food_data("banana")