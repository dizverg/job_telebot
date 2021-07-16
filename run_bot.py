import logging
from aiogram.utils import executor

from config import LOG
from telechatbot.bot_dispatcher import dispatcher as dp

logging.basicConfig(**LOG)

if __name__ == '__main__':
    executor.start_polling(dp)
