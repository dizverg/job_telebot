from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher

from cfg.config import TOKEN, TOKENS


applicant_bot = Bot(token=TOKENS['applicant_ui'])
publisher_bot = Bot(token=TOKENS['publisher_ui'])
# hr_bot = Bot(token=tokens['hr_ui'])


bot = Bot(token=TOKEN)
bot_dispatcher = Dispatcher(bot, storage=MemoryStorage())
bot_dispatcher.middleware.setup(LoggingMiddleware())
