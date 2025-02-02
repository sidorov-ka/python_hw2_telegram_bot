def format_progress_text(water_norm, logged_water, calorie_norm, logged_calories, burned_calories):
    """
    Форматирует текст прогресса пользователя.

    :param water_norm: Норма воды (мл).
    :param logged_water: Записанное потребление воды (мл).
    :param calorie_norm: Норма калорий (ккал).
    :param logged_calories: Записанное потребление калорий (ккал).
    :param burned_calories: Сожжённые калории (ккал).
    :return: Отформатированный текст прогресса.
    """
    if water_norm is None or calorie_norm is None:
        return "⚠️ Сначала настройте профиль с помощью /set_profile."

    # Приводим числа к `int`, чтобы избежать лишних `.0`
    water_norm, logged_water = int(water_norm), int(logged_water)
    calorie_norm, logged_calories, burned_calories = (
        int(calorie_norm), int(logged_calories), int(burned_calories)
    )

    return f"""
📊 *Ваш прогресс*:

💧 *Вода*:
- Выпито: {logged_water} мл / {water_norm} мл
- Осталось: {max(0, water_norm - logged_water)} мл

🔥 *Калории*:
- Потреблено: {logged_calories} ккал / {calorie_norm} ккал
- Сожжено: {burned_calories} ккал
- Баланс: {logged_calories - burned_calories} ккал
"""
