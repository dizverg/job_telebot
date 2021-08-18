from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import ContentTypes, Message
from cfg.main_menu import PUBLISHER_MENU, APPLICANT_MENU
import logging
from aiogram.utils import executor

from lib.bot_dispatcher import bot_dispatcher
from cfg.config import LOG, MODE
from cfg.callback_for_inline_buttons import applicant_respond_callback, \
    hr_respond_callback, \
    show_user_link_respond_callback

from dialogs.respond_dialog import RespondDialog
from dialogs.publisher_dialog import PublisherDialog

logging.basicConfig(**LOG)


def register_main_menu_handlers(main_menu):
    for key, value in main_menu.items():
        bot_dispatcher.register_message_handler(
            value.get("action", None), commands=key, state='*')


async def default_answer(message: Message, state: FSMContext):
    await message.answer(" ")


if __name__ == '__main__':

    # bot_dispatcher.register_message_handler(default_answer)

    if MODE == 'publisher_ui':
        register_main_menu_handlers(PUBLISHER_MENU)

        bot_dispatcher.register_message_handler(
            PublisherDialog.get_text_answer,
            state=[PublisherDialog.States.questions,
                   PublisherDialog.States.description],
            content_types=['text'])

        # bot_dispatcher.register_message_handler(
        #     PublisherDialog.get_text_answer,
        #     state='*')

        bot_dispatcher.register_message_handler(
            PublisherDialog.get_photo_answer,
            state=PublisherDialog.States.photo,
            content_types=['photo'])

    elif MODE == 'applicant_ui':
        register_main_menu_handlers(APPLICANT_MENU)

        bot_dispatcher.register_message_handler(
            RespondDialog.get_text_answer,
            state=RespondDialog.States,
            content_types=['text'])

        # bot_dispatcher.register_message_handler(
        #     RespondDialog.get_text_answer,
        #     state='*',
        #     content_types=['text'])

        bot_dispatcher.register_message_handler(
            RespondDialog.get_video_answer,
            # state='*',
            state=RespondDialog.States,
            content_types=ContentTypes.VIDEO_NOTE
        )

        bot_dispatcher.register_callback_query_handler(
            applicant_respond_callback,
            lambda query: query.data.startswith('respond'), state="*")

        # elif MODE == 'hr_ui':
        bot_dispatcher.register_callback_query_handler(
            show_user_link_respond_callback,
            lambda query: query.data.startswith('show_user_link'), state="*")

        bot_dispatcher.register_callback_query_handler(
            hr_respond_callback,
            lambda query: query.data.startswith('reject'), state="*")


    @bot_dispatcher.callback_query_handler()
    async def default_callback(callback_query: CallbackQuery):
        await bot_dispatcher.bot.answer_callback_query(callback_query.id)

    executor.start_polling(bot_dispatcher)

    # asyncio.run(send_message())
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(
    #     applicant_bot.send_message( CHANNEL_ID,'test3'))
# asyncio.set_event_loop(loop)
# loop.run_until_complete(
# executor.start_polling(bot_dispatcher))
