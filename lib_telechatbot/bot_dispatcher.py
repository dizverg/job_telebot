from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from private_token import TOKEN, token



bot = Bot(token=TOKEN)
applicant_bot = Bot(token=token['applicant_ui'])

bot_dispatcher = Dispatcher(bot, storage=MemoryStorage())
bot_dispatcher.middleware.setup(LoggingMiddleware())








