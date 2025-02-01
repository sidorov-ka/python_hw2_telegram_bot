import aiosqlite
import asyncio
from typing import Optional, Any, Dict

DATABASE = 'user_data.db'

async def create_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                weight REAL,
                height INTEGER,
                age INTEGER,
                activity INTEGER,
                city TEXT,
                gender TEXT CHECK(gender IN ('male', 'female')), -- Добавлено поле gender
                water_goal INTEGER DEFAULT 2400,
                calorie_goal INTEGER DEFAULT 2500,
                logged_water INTEGER DEFAULT 0,
                logged_calories INTEGER DEFAULT 0,
                burned_calories INTEGER DEFAULT 0
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS food_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                food_name TEXT,
                quantity INTEGER,
                calories REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def insert_user(user_id: int, weight: float, height: int, age: int, activity: int, city: str, gender: str,
                      water_goal: int = 2400, calorie_goal: int = 2500):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            INSERT INTO users (user_id, weight, height, age, activity, city, gender, water_goal, calorie_goal, logged_water, logged_calories, burned_calories)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0)
        ''', (user_id, weight, height, age, activity, city, gender, water_goal, calorie_goal))
        await db.commit()

async def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def update_user(user_id: int, field: str, value: Any):
    allowed_fields = {
        "weight", "height", "age", "activity", "city", "gender",
        "water_goal", "calorie_goal", "logged_water", "logged_calories", "burned_calories"
    }
    if field not in allowed_fields:
        raise ValueError(f"Недопустимое поле: {field}")

    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(f'UPDATE users SET {field} = ? WHERE user_id = ?', (value, user_id))
        await db.commit()

async def log_food_entry(user_id: int, food_name: str, quantity: int, calories: float):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            INSERT INTO food_log (user_id, food_name, quantity, calories)
            VALUES (?, ?, ?, ?)
        ''', (user_id, food_name, quantity, calories))
        await db.commit()

async def get_food_log(user_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM food_log WHERE user_id = ? ORDER BY timestamp DESC', (user_id,)) as cursor:
            return [dict(row) async for row in cursor]

# Пример вызова для тестирования
if __name__ == '__main__':
    asyncio.run(create_db())
    asyncio.run(insert_user(123456, 70.5, 175, 25, 30, 'Moscow', 'male'))
