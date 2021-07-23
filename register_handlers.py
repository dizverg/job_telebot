
import asyncio
import logging

from aiogram.dispatcher.filters.state import State
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils import executor

from config import CHANEL_ID, LOG, MODE
from dialogs.publush_dialog import PublishDialog
from dialogs.respond_dialog import RespondDialog
from lib_telechatbot.bot_dispatcher import (applicant_bot, bot, bot_dispatcher,
                                            publisher_bot)
from lib_telechatbot.dialog import Dialog
from main_menu_actions import register_main_menu_handlers
from messages import MAIN_MENU
from models.Vacanse import Vacanse

callback = {
    # 'applicant_ui': applicant_callbac
}

publish_dialog = PublishDialog()

def register_handlers():

    register_main_menu_handlers()

    register_callback_query_handlers()




def register_main_menu_handlers():
        for key, value in MAIN_MENU.items():
            bot_dispatcher.register_message_handler(
                value.get("action", None), commands=key)


def register_callback_query_handlers():  


    async def default_callback(callback_query: CallbackQuery):
        await bot.answer_callback_query(callback_query.id)

    bot_dispatcher.register_callback_query_handler(
        callback.get(MODE, default_callback), 
        lambda query: query.data.startswith(MODE)
    )

    bot_dispatcher.register_callback_query_handler(default_callback)

