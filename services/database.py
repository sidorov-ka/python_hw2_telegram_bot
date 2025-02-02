import json
import threading

# Файл для хранения данных
DB_FILE = "user_data.json"
_lock = threading.Lock()  # Блокировка для потокобезопасной записи

# Загружаем данные из файла при запуске
try:
    with open(DB_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    users = {}  # Если файла нет или ошибка в JSON, создаём пустую базу


def get_user_data(user_id):
    """
    Получает данные пользователя.

    :param user_id: ID пользователя.
    :return: Данные пользователя или None, если не найден.
    """
    return users.get(str(user_id))


def get_or_create_user_data(user_id):
    """
    Получает данные пользователя или создаёт новую запись.

    :param user_id: ID пользователя.
    :return: Данные пользователя.
    """
    user_id = str(user_id)
    if user_id not in users:
        users[user_id] = {
            "weight": 0,
            "height": 0,
            "age": 0,
            "activity": 0,
            "logged_water": 0,
            "logged_calories": 0,
            "burned_calories": 0,
            "city": "",
        }
        save_user_data(user_id, users[user_id])
    return users[user_id]


def save_user_data(user_id, data):
    """
    Сохраняет данные пользователя и записывает их в JSON-файл.

    :param user_id: ID пользователя.
    :param data: Данные пользователя (словарь).
    """
    user_id = str(user_id)
    users[user_id] = data  # Приводим ID к строке для удобства

    # Используем блокировку для безопасной записи
    with _lock:
        try:
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
