
import asyncio

from aiogram.dispatcher.filters.state import State
from dialogs.respond_dialog import RespondDialog
from models.Vacanse import Vacanse
from lib_telechatbot.dialog import Dialog

from aiogram.types.callback_query import CallbackQuery
from dialogs.publush_dialog import PublishDialog
import logging
from main_menu_actions import register_main_menu_handlers
from messages import MAIN_MENU
from aiogram.utils import executor
from lib_telechatbot.bot_dispatcher import bot_dispatcher, bot, applicant_bot, publisher_bot
from config import CHANEL_ID, LOG, MODE

callback = {

}


def register_handlers():
    
    if MODE == 'publisher_ui':
         PublishDialog.register_handlers()

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

