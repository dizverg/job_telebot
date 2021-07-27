from aiogram.types.callback_query import CallbackQuery

from lib.bot_dispatcher import bot_dispatcher



def register_main_menu_handlers(main_menu):
    for key, value in main_menu.items():
        bot_dispatcher.register_message_handler(
            value.get("action", None), commands=key)


def register_callback_query_handlers(callback_for_inline_buttons, mode):

    async def default_callback(callback_query: CallbackQuery):
        await bot_dispatcher.bot.answer_callback_query(callback_query.id)

    current_callback = callback_for_inline_buttons.get(mode, default_callback)
    bot_dispatcher.register_callback_query_handler(
        current_callback, lambda query: query.data.startswith(mode), state="*")

    bot_dispatcher.register_callback_query_handler(default_callback)
