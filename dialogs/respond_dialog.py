

from io import BytesIO
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import callback_query, video
from lib_telechatbot.dialog import Dialog, reg

from aiogram.types.callback_query import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from sqlalchemy.sql.expression import text
from config import CHANEL_ID
from messages import DIALOGS
from models import Vacanse
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message
from dialogs.base_dialog import BaseDialog
from lib_telechatbot.bot_dispatcher import bot, applicant_bot, bot_dispatcher



class RespondDialog(BaseDialog):    
    def __init__(self, config, from_user) -> None:
        super().__init__(config, from_user)
        self.config = config
        self.from_user = from_user
        self.dialog = Dialog(config=self.config, bot=applicant_bot)


    def register_handlers(self):
        
        bot_dispatcher.register_message_handler(
            callback=self.answer_callback,
            state=reg.st,
            content_types=['text'])

        bot_dispatcher.register_message_handler(
            callback=self.video_callback,
            state=reg.st,
            content_types=['video'])

    async def begin(self):

        await self.dialog.ask(self.from_user.id, self.config[0], state = reg.st)

    async def answer_callback(
            self, message: Message, state: FSMContext, *arrgs, **kwargs):
        await self.get_answer(message, state, self.finish)

    async def video_callback(
            self, message: Message, state: FSMContext, *arrgs, **kwargs):
        file_id = message.video[-1].file_id
        await state.update_data({'file_id': file_id})
        await self.get_answer(message, state, self.finish)

    async def finish(self, message: Message, state: FSMContext):
        data = await state.get_data()
        user_id = await self.get_user_id()
        if not user_id:
            await message.answer('error',
                                 reply_markup=ReplyKeyboardRemove())
            return

        file_id = data.get('file_id')
        if file_id:
            file: BytesIO = await bot.download_file_by_id(file_id)

        discriptions = data.get('discription')
        questions = data.get('questions')
        await message.answer(questions)

        # vacanse = Vacanse(
        #     photo=file_id,
        #     discriptions=discriptions,
        #     questions=questions,
        #     user_id=user_id)

        # if file_id or discriptions or questions:
        #     vacanse.add()

        # discription = vacanse.get_discription()
        # await message.answer()
        # # show_preview_to_publicher
        # await message.answer_video(video=file_id, caption=vacanse,
        #                            reply_markup=ReplyKeyboardRemove())

        # # publishing to chanel
        # await applicant_bot.send_video(
        #     CHANEL_ID,
        #     video=await bot.download_file_by_id(data.get('file_id')),
        #     caption=discription or '-',
        #     reply_markup=InlineKeyboardMarkup().add(
        #         InlineKeyboardButton(
        #             'Отклонить', callback_data=f'reject {vacanse.id}')))

        state.finish()