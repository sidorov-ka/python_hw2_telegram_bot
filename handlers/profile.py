from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.fsm.context import FSMContext
from states import ProfileStates
from database import insert_user, update_user, get_user

async def set_profile_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await get_user(user_id)

    if user_data:
        await message.answer("Ваш профиль уже заполнен. Хотите обновить данные? (напишите /reset_profile)")
        return

    await message.answer("Введите ваш вес (в кг):")
    await state.set_state(ProfileStates.weight)

async def set_profile_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        await state.update_data(weight=weight)
        await message.answer("Введите ваш рост (в см):")
        await state.set_state(ProfileStates.height)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")

async def set_profile_height(message: types.Message, state: FSMContext):
    try:
        height = int(message.text)
        await state.update_data(height=height)
        await message.answer("Введите ваш возраст:")
        await state.set_state(ProfileStates.age)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")

async def set_profile_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await message.answer("Сколько минут активности у вас в день?")
        await state.set_state(ProfileStates.activity)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")

async def set_profile_activity(message: types.Message, state: FSMContext):
    try:
        activity = int(message.text)
        await state.update_data(activity=activity)
        await message.answer("В каком городе вы находитесь?")
        await state.set_state(ProfileStates.city)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")

async def set_profile_city(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    city = message.text
    weight = data.get("weight")
    height = data.get("height")
    age = data.get("age")
    activity = data.get("activity")

    water_goal, calorie_goal = calculate_goals(weight, height, age, activity)

    await insert_user(user_id, weight, height, age, activity, city, water_goal, calorie_goal)

    await message.answer(f"Профиль настроен!\n💧 Ваша дневная норма воды: {water_goal} мл\n🔥 Ваша дневная норма калорий: {calorie_goal} ккал")
    await state.clear()


def calculate_goals(weight, height, age, activity, gender):
    water_goal = round(weight * 35)  # 35 мл на кг массы

    if gender == "male":
        calorie_goal = round((10 * weight) + (6.25 * height) - (5 * age) + 5 + (activity * 10))
    else:
        calorie_goal = round((10 * weight) + (6.25 * height) - (5 * age) - 161 + (activity * 10))

    return water_goal, calorie_goal

def register_profile_handlers(dp: Dispatcher):
    dp.register_message_handler(set_profile_start, commands="set_profile")
    dp.register_message_handler(set_profile_weight, state=ProfileStates.weight)
    dp.register_message_handler(set_profile_height, state=ProfileStates.height)
    dp.register_message_handler(set_profile_age, state=ProfileStates.age)
    dp.register_message_handler(set_profile_activity, state=ProfileStates.activity)
    dp.register_message_handler(set_profile_city, state=ProfileStates.city)
