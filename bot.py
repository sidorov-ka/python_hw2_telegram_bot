import asyncio
from utils.config import TELEGRAM_BOT_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

# Инициализируем бота с HTML-разметкой по умолчанию
bot = Bot(
    token=TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Инициализируем диспетчер
dp = Dispatcher()

# Импортируем роутеры из хендлеров
from handlers.profile_handlers import router as profile_router
from handlers.log_handlers import router as log_router
from handlers.progress_handlers import router as progress_router

# Подключаем роутеры
dp.include_router(profile_router)
dp.include_router(log_router)
dp.include_router(progress_router)

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я бот для расчёта нормы воды, калорий и трекинга активности.\n"
        "Используй /help для списка команд."
    )

# Обработчик команды /help
@dp.message(Command("help"))
async def help(message: Message):
    help_text = """
<b>Доступные команды:</b>
/start - Начать работу с ботом
/help - Получить список команд
/set_profile - Настроить профиль
/log_water - Записать потребление воды
/log_food - Записать потребление еды
/log_workout - Записать тренировку
/check_progress - Проверить прогресс
"""
    await message.answer(help_text)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
