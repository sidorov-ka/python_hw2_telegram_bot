from aiogram.fsm.state import State, StatesGroup

class ProfileStates(StatesGroup):
    weight = State()  # Состояние для веса
    height = State()  # Состояние для роста
    age = State()  # Состояние для возраста
    activity = State()  # Состояние для активности
    city = State()  # Состояние для города
    confirm = State()  # Подтверждение данных профиля

class FoodStates(StatesGroup):
    food_name = State()  # Ввод названия продукта
    food_quantity = State()  # Ввод количества
    confirm = State()  # Подтверждение

class WaterStates(StatesGroup):
    water_quantity = State()  # Ввод количества воды
    confirm = State()  # Подтверждение

class WorkoutStates(StatesGroup):
    workout_type = State()  # Тип тренировки
    workout_duration = State()  # Длительность
    confirm = State()  # Подтверждение
