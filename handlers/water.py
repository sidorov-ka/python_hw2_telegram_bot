from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.fsm.context import FSMContext
from states import WaterStates
from database import get_user, update_user

async def log_water(message: types.Message, state: FSMContext):
    """Запрос количества выпитой воды."""
    await message.answer("Сколько воды вы выпили? (в мл)")
    await state.set_state(WaterStates.water_quantity)

async def log_water_quantity(message: types.Message, state: FSMContext):
    """Обновление количества выпитой воды в БД."""
    user_id = message.from_user.id

    try:
        water = int(message.text)
        if water <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Введите корректное количество воды (целое число в мл).")
        return

    user_data = await get_user(user_id)

    if not user_data:
        await message.answer("Ошибка: ваш профиль не найден. Используйте /set_profile для его создания.")
        await state.clear()
        return

    current_water = user_data["logged_water"]
    water_goal = user_data["water_goal"]

    new_total = current_water + water

    # Обновляем БД
    await update_user(user_id, "logged_water", new_total)

    # Сообщаем пользователю прогресс
    if new_total >= water_goal:
        await message.answer(f"🎉 Вы достигли дневной нормы воды! ({new_total}/{water_goal} мл) Отличная работа! 💧")
    else:
        remaining = water_goal - new_total
        await message.answer(f"✅ Добавлено {water} мл. Всего выпито: {new_total}/{water_goal} мл.\n"
                             f"Осталось: {remaining} мл до цели! 💪")

    await state.clear()

def register_water_handlers(dp: Dispatcher):
    """Регистрирует обработчики команд."""
    dp.register_message_handler(log_water, Command("log_water"))
    dp.register_message_handler(log_water_quantity, state=WaterStates.water_quantity)
