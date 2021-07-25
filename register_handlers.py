from aiogram.types.callback_query import CallbackQuery
from config import MODE
from lib.bot_dispatcher import bot, bot_dispatcher
from messages import MAIN_MENU
from respond_dialog import applicant_respond_callback


callback = {
    'applicant_ui': applicant_respond_callback
}

# publish_dialog = PublishDialog()


def register_main_menu_handlers():
    for key, value in MAIN_MENU.items():
        bot_dispatcher.register_message_handler(
            value.get("action", None), commands=key)


def register_callback_query_handlers():

    async def default_callback(callback_query: CallbackQuery):
        await bot.answer_callback_query(callback_query.id)

    current_callback = callback.get(MODE, default_callback)
    bot_dispatcher.register_callback_query_handler(
        current_callback, lambda query: query.data.startswith(MODE), state="*")

    bot_dispatcher.register_callback_query_handler(default_callback)
