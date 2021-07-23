

from config import MODE
from io import BytesIO
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import callback_query, video
from lib_telechatbot.dialog import Dialog

from aiogram.types.callback_query import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from sqlalchemy.sql.expression import text
from models import Vacanse
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message
from dialogs.base_dialog import BaseDialog
from lib_telechatbot.bot_dispatcher import bot, applicant_bot, bot_dispatcher


async def respond_callback(callback_query: CallbackQuery):
        vacanse_id = callback_query.data.split(' ')[1]

        dialog =RespondDialog(
            config = Vacanse.find_by_id(vacanse_id).questions,
            from_user =callback_query.from_user
        )
        dialog.register_handlers()

        await dialog.begin()
        
        await bot.answer_callback_query(callback_query.id)

        # await bot.send_message(callback_query.from_user.id, callback_query.data)
        # await applicant_bot.answer_callback_query(
        #     callback_query.id, text=callback_query.data, show_alert=True)


class RespondDialog(BaseDialog):    
    def __init__(self, config) -> None:
        super().__init__(applicant_bot, config)

        if MODE == 'applicant_ui':
            self.register_handlers()


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
