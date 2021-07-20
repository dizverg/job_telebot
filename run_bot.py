import asyncio

from asyncio.base_events import _run_until_complete_cb
from private_token import TOKEN
from dialogs.publush_dialog import PublishDialog
import logging
from main_menu_actions import register_main_menu_handlers
from messages import MAIN_MENU
from aiogram.utils import executor
from lib_telechatbot.bot_dispatcher import bot_dispatcher

from config import LOG

logging.basicConfig(**LOG)


if __name__ == '__main__':
    register_main_menu_handlers()
    PublishDialog().register_handlers()

    executor.start_polling(bot_dispatcher)
    
    