import logging
from main_menu_actions import MAIN_MENU
from aiogram.utils import executor

from lib.bot_dispatcher import bot_dispatcher
from config import LOG
from register_handlers import register_main_menu_handlers, register_callback_query_handlers

logging.basicConfig(**LOG)

def register_main_menu_handlers():
    for key, value in MAIN_MENU.items():
        bot_dispatcher.register_message_handler(
            value.get("action", None), commands=key)
            
if __name__ == '__main__':

    register_main_menu_handlers()
    

    register_callback_query_handlers()
    
    executor.start_polling(bot_dispatcher)


    # asyncio.run(send_message())
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(
    #     applicant_bot.send_message( CHANEL_ID,'test3'))
   # asyncio.set_event_loop(loop)
    # loop.run_until_complete(
    # executor.start_polling(bot_dispatcher))
