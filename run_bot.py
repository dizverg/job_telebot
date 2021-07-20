import asyncio
from dialogs.publush_dialog import PublishDialog
import logging
from main_menu_actions import register_main_menu_handlers
from messages import MAIN_MENU
from aiogram.utils import executor
from lib_telechatbot.bot_dispatcher import bot_dispatcher, bot, applicant_bot
from config import CHANEL_ID, LOG

logging.basicConfig(**LOG)



if __name__ == '__main__':
    register_main_menu_handlers(bot_dispatcher)
    PublishDialog().register_handlers(bot_dispatcher)
    # asyncio.run(send_message())
    loop = asyncio.new_event_loop()
    # loop.run_until_complete(
    #     applicant_bot.send_message( CHANEL_ID,'test3'))
   # asyncio.set_event_loop(loop)
    loop.run_until_complete(
        executor.start_polling(bot_dispatcher))
    executor.start_polling(bot_dispatcher)
    
    