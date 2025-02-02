from aiogram.fsm.state import State, StatesGroup

class ProfileStates(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity = State()
    city = State()
    confirm = State()

class FoodStates(StatesGroup):
    name = State()  # Ввод названия продукта
    quantity = State()  # Ввод количества

class WaterStates(StatesGroup):
    quantity = State()  # Ввод количества воды

class WorkoutStates(StatesGroup):
    type = State()  # Тип тренировки
    duration = State()  # Длительность
