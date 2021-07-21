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
from config import CHANEL_ID, LOG

logging.basicConfig(**LOG)


@bot_dispatcher.callback_query_handler(
    lambda query: query.data.startswith("respond"))
async def respond_callback(callback_query: CallbackQuery):
    vacanse_id = callback_query.data.split(' ')[1]

    dialog =RespondDialog(
        config = Vacanse.find_by_id(vacanse_id).questions,
        from_user =callback_query.from_user
    )
    dialog.register_handlers()

    await dialog.begin()
    

    await bot.answer_callback_query(callback_query.id)

    # await bot.send_message(callback_query.from_user.id, callback_query.data)
    # await applicant_bot.answer_callback_query(
    #     callback_query.id, text=callback_query.data, show_alert=True)


@bot_dispatcher.callback_query_handler()
async def default_callback(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)


if __name__ == '__main__':

    register_main_menu_handlers()
    # PublishDialog.register_handlers()

    executor.start_polling(bot_dispatcher)

    # asyncio.run(send_message())
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(
    #     applicant_bot.send_message( CHANEL_ID,'test3'))
   # asyncio.set_event_loop(loop)
    # loop.run_until_complete(
    # executor.start_polling(bot_dispatcher))
