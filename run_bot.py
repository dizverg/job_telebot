from dialogs.publisher_dialog import PublishStates, PublisherDialog
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
from cfg.main_menu import DEFAULT_MENU, PUBLISHER_MENU
import logging
from aiogram.utils import executor

from lib.bot_dispatcher import bot_dispatcher
from cfg.config import LOG, MODE
from cfg.callback_for_inline_buttons import applicant_respond_callback

logging.basicConfig(**LOG)


def register_main_menu_handlers(main_menu):
    for key, value in main_menu.items():
        bot_dispatcher.register_message_handler(
            value.get("action", None), commands=key)



if __name__ == '__main__':

    if MODE == 'publisher_ui':
        register_main_menu_handlers(PUBLISHER_MENU)
        
        bot_dispatcher.register_message_handler(
            PublisherDialog.get_text_answer, 
            state=[PublishStates.questions, PublishStates.discription],
            content_types=['text'])
        
        # bot_dispatcher.register_message_handler(
        #     PublisherDialog.get_text_answer, 
        #     state='*')

        bot_dispatcher.register_message_handler(
            PublisherDialog.get_photo_answer, state=PublishStates.photo, 
            content_types=['photo'])


    bot_dispatcher.register_callback_query_handler(
        applicant_respond_callback,
        lambda query: query.data.startswith(MODE), state="*")

    register_main_menu_handlers(DEFAULT_MENU)

    @bot_dispatcher.callback_query_handler()
    async def default_callback(callback_query: CallbackQuery):
        await bot_dispatcher.bot.answer_callback_query(callback_query.id)

    executor.start_polling(bot_dispatcher)

    # asyncio.run(send_message())
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(
    #     applicant_bot.send_message( CHANEL_ID,'test3'))
   # asyncio.set_event_loop(loop)
    # loop.run_until_complete(
    # executor.start_polling(bot_dispatcher))
