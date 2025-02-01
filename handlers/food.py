from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.fsm.context import FSMContext
from states import FoodStates
from services.food_api import get_food_data
from database import log_food_entry

async def log_food(message: types.Message, state: FSMContext):
    args = message.text.split(' ', 1)
    if len(args) < 2:
        await message.answer("Пожалуйста, укажите название продукта после команды. Например: /log_food яблоко")
        return

    product_name = args[1].lower()
    await state.update_data(food_name=product_name)  # Сохраняем название продукта в состояние

    food_data = await get_food_data(product_name)  # Асинхронный вызов

    if "error" in food_data:
        await message.answer(f"Ошибка: {food_data['error']}")
        return

    calories = food_data.get('nutriments', {}).get('energy_kcal', 0)
    if calories:
        await message.answer(f"Продукт {product_name} — {calories} ккал на 100 г. Сколько грамм вы съели?")
        await state.set_state(FoodStates.food_quantity)  # Устанавливаем следующее состояние
    else:
        await message.answer(f"Не удалось найти калорийность для продукта {product_name}.")

async def log_food_final(message: types.Message, state: FSMContext):
    data = await state.get_data()
    food_name = data.get('food_name')

    try:
        quantity = float(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")
        return

    food_data = await get_food_data(food_name)  # Асинхронный вызов
    calories_per_100g = food_data.get('nutriments', {}).get('energy_kcal', 0)

    if not calories_per_100g:
        await message.answer(f"Не удалось получить калорийность для {food_name}.")
        await state.clear()
        return

    total_calories = (calories_per_100g * quantity) / 100

    await log_food_entry(message.from_user.id, food_name, quantity, total_calories)  # Сохраняем в БД

    await message.answer(f"Вы съели {quantity} г {food_name}, это {total_calories:.2f} ккал.")
    await state.clear()

def register_food_handlers(dp: Dispatcher):
    dp.register_message_handler(log_food, Command("log_food"))
    dp.register_message_handler(log_food_final, state=FoodStates.food_quantity)
