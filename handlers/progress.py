from aiogram import types
from aiogram.fsm.context import FSMContext
from database import update_user, get_user, log_food_entry


async def log_water_intake(message: types.Message):
    """Добавляет количество выпитой воды пользователю."""
    user_id = message.from_user.id

    try:
        water_amount = int(message.text)
        if water_amount <= 0:
            raise ValueError

        user_data = await get_user(user_id)
        if not user_data:
            await message.answer("Сначала настройте профиль: /set_profile")
            return

        new_logged_water = user_data["logged_water"] + water_amount
        await update_user(user_id, "logged_water", new_logged_water)

        await message.answer(f"💧 Вы записали {water_amount} мл воды!\n"
                             f"Всего за день: {new_logged_water} мл из {user_data['water_goal']} мл.")
    except ValueError:
        await message.answer("Введите количество воды в миллилитрах (например, 250).")


async def log_food_intake(message: types.Message, state: FSMContext):
    """Добавляет запись о приеме пищи в БД."""
    user_id = message.from_user.id
    food_data = message.text.split(",")

    if len(food_data) != 3:
        await message.answer("Введите данные в формате: Название, Количество(г), Калории (например: Яблоко, 150, 80)")
        return

    try:
        food_name = food_data[0].strip()
        quantity = int(food_data[1].strip())
        calories = float(food_data[2].strip())

        await log_food_entry(user_id, food_name, quantity, calories)

        user_data = await get_user(user_id)
        new_logged_calories = user_data["logged_calories"] + calories
        await update_user(user_id, "logged_calories", new_logged_calories)

        await message.answer(f"🍎 Вы добавили: {food_name} ({quantity}г, {calories} ккал)\n"
                             f"Всего за день: {new_logged_calories} из {user_data['calorie_goal']} ккал.")
    except ValueError:
        await message.answer("Ошибка в формате. Введите данные в формате: Название, Количество(г), Калории")


async def log_burned_calories(message: types.Message):
    """Добавляет количество сожжённых калорий."""
    user_id = message.from_user.id

    try:
        burned_calories = int(message.text)
        if burned_calories <= 0:
            raise ValueError

        user_data = await get_user(user_id)
        if not user_data:
            await message.answer("Сначала настройте профиль: /set_profile")
            return

        new_burned_calories = user_data["burned_calories"] + burned_calories
        await update_user(user_id, "burned_calories", new_burned_calories)

        await message.answer(f"🔥 Вы записали {burned_calories} ккал как сожженные!\n"
                             f"Всего за день: {new_burned_calories} ккал.")
    except ValueError:
        await message.answer("Введите количество сожжённых калорий числом (например, 300).")


async def get_progress(message: types.Message):
    """Отправляет пользователю текущий прогресс за день."""
    user_id = message.from_user.id
    user_data = await get_user(user_id)

    if not user_data:
        await message.answer("Сначала настройте профиль: /set_profile")
        return

    progress_message = (f"📊 *Ваш прогресс за сегодня:*\n"
                        f"💧 Вода: {user_data['logged_water']} / {user_data['water_goal']} мл\n"
                        f"🔥 Калории: {user_data['logged_calories']} / {user_data['calorie_goal']} ккал\n"
                        f"⚡ Сожженные калории: {user_data['burned_calories']} ккал")

    await message.answer(progress_message, parse_mode="Markdown")


def register_progress_handlers(dp):
    """Регистрирует обработчики для логирования прогресса."""
    dp.register_message_handler(log_water_intake, commands="log_water")
    dp.register_message_handler(log_food_intake, commands="log_food")
    dp.register_message_handler(log_burned_calories, commands="log_burned")
    dp.register_message_handler(get_progress, commands="progress")
