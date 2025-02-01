import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import API_TOKEN
from handlers.profile import register_profile_handlers
from handlers.food import register_food_handlers
from handlers.water import register_water_handlers
from handlers.workout import register_workout_handlers
from handlers.progress import register_progress_handlers  # Новый импорт
from middlewares.logging import LogMiddleware

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Регистрируем middleware
    dp.update.middleware(LogMiddleware())

    # Регистрируем хендлеры
    register_profile_handlers(dp)
    register_food_handlers(dp)
    register_water_handlers(dp)
    register_workout_handlers(dp)
    register_progress_handlers(dp)

    # Устанавливаем команды бота
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="progress", description="Ваш дневной прогресс"),  # Новая команда
    ])

    # Запускаем бота
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
