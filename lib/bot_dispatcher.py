from config import TOKEN
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from private_token import tokens


bot = Bot(token=TOKEN)
applicant_bot = Bot(token=tokens['applicant_ui'])
publisher_bot = Bot(token=tokens['publisher_ui'])
hr_bot = Bot(token=tokens['hr_ui'])

bot_dispatcher = Dispatcher(bot, storage=MemoryStorage())
bot_dispatcher.middleware.setup(LoggingMiddleware())
