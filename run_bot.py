from cfg.main_menu import DEFAULT_MENU, PUBLISHER_MENU
import logging
from aiogram.utils import executor

from lib.bot_dispatcher import bot_dispatcher
from cfg.config import LOG, MODE
from lib.register_handlers import register_main_menu_handlers, register_callback_query_handlers
from cfg.callback_for_inline_buttons import CALLBACKS

logging.basicConfig(**LOG)


if __name__ == '__main__':

    register_main_menu_handlers(
        {**(PUBLISHER_MENU if MODE == 'publisher_ui' else dict()),
            **DEFAULT_MENU}
    )

    register_callback_query_handlers(
        CALLBACKS, MODE
    )

    executor.start_polling(bot_dispatcher)

    # asyncio.run(send_message())
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(
    #     applicant_bot.send_message( CHANEL_ID,'test3'))
   # asyncio.set_event_loop(loop)
    # loop.run_until_complete(
    # executor.start_polling(bot_dispatcher))
