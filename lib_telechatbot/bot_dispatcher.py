from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher

from private_token import TOKEN

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
dispatcher.middleware.setup(LoggingMiddleware())
