import logging
from aiogram.utils import executor

from lib_telechatbot.bot_dispatcher import bot_dispatcher
from config import LOG
from register_handlers import register_handlers

logging.basicConfig(**LOG)

if __name__ == '__main__':
    register_handlers()
    executor.start_polling(bot_dispatcher)


    # asyncio.run(send_message())
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(
    #     applicant_bot.send_message( CHANEL_ID,'test3'))
   # asyncio.set_event_loop(loop)
    # loop.run_until_complete(
    # executor.start_polling(bot_dispatcher))
