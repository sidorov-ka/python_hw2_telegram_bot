def calculate_water_norm(user_data, temperature):
    """
    Рассчитывает норму воды с учётом температуры.

    :param user_data: Словарь с данными пользователя (вес, активность).
    :param temperature: Текущая температура в городе пользователя.
    :return: Рекомендуемая норма воды в мл.
    """
    weight = user_data.get("weight", 0)
    activity = user_data.get("activity", 0)

    if not weight:
        return None  # Если веса нет, расчёт невозможен

    base_norm = weight * 30  # 30 мл на 1 кг веса
    activity_norm = (activity // 30) * 500  # +500 мл за каждые 30 минут активности

    # Коррекция нормы воды в зависимости от температуры
    if temperature > 30:
        temp_adjustment = 1000  # +1000 мл при >30°C
    elif temperature > 25:
        temp_adjustment = 500  # +500 мл при >25°C
    elif temperature < 5:
        temp_adjustment = -0.1 * base_norm  # -10% от базовой нормы при <5°C
    else:
        temp_adjustment = 0

    return base_norm + activity_norm + temp_adjustment


def calculate_calorie_norm(user_data):
    """
    Рассчитывает норму калорий по формуле Миффлина-Сан Жеора.

    :param user_data: Словарь с данными пользователя (вес, рост, возраст, активность).
    :return: Рекомендуемая суточная норма калорий.
    """
    weight = user_data.get("weight", 0)
    height = user_data.get("height", 0)
    age = user_data.get("age", 0)
    activity = user_data.get("activity", 0)

    if not all([weight, height, age]):
        return None  # Если нет ключевых данных, расчёт невозможен

    # Формула Миффлина-Сан Жеора без учёта пола (можно расширить)
    calorie_norm = 10 * weight + 6.25 * height - 5 * age
    calorie_norm += activity * 5  # +5 ккал за каждую минуту активности

    return calorie_norm
