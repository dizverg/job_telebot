
from aiogram.dispatcher.filters.state import State
from aiogram.types.callback_query import CallbackQuery


from config import MODE
from publush_dialog import PublishDialog
from lib_telechatbot.bot_dispatcher import bot, bot_dispatcher

from messages import MAIN_MENU

from dialogs.respond_dialog import respond_callback

callback = {
    'applicant_ui': respond_callback
}

publish_dialog = PublishDialog()


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

