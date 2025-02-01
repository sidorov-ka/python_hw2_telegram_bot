from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
import logging
from database import get_user, update_user  # Импортируем функции из базы данных

logging.basicConfig(level=logging.INFO)

class LogMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: types.Message, data: dict):
        user_id = event.from_user.id
        text = event.text
        logging.info(f"User {user_id} sent message: {text}")

        user_data = await get_user(user_id)
        if user_data:
            if "вода" in text.lower():
                current_water = user_data['logged_water']
                await update_user(user_id, 'logged_water', current_water + 200)
            logging.info(f"User {user_id} data updated: {user_data}")
        else:
            logging.info(f"User {user_id} not found in DB.")

        return await handler(event, data)
