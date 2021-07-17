from dialogs.publush_dialog import PublishDialog
import logging
from main_menu_actions import register_main_menu_handlers
from messages import MAIN_MENU
from aiogram.utils import executor

from config import LOG
from lib_telechatbot.bot_dispatcher import bot_dispatcher 

logging.basicConfig(**LOG)


if __name__ == '__main__':
    register_main_menu_handlers()
    PublishDialog().register_handlers()

    executor.start_polling(bot_dispatcher)
