import logging
from messages import MAIN_MENU
from aiogram.utils import executor

from config import LOG
from telechatbot.bot_dispatcher import dispatcher as dp

logging.basicConfig(**LOG)

for key, value in MAIN_MENU.items():
    dp.register_message_handler(value.get("action",None), commands=key)


if __name__ == '__main__':
    executor.start_polling(dp)
