

from io import BytesIO
from lib_telechatbot.dialog import Dialog
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from sqlalchemy.sql.expression import text
from config import CHANEL_ID, MODE
from messages import DIALOGS
from models import Vacanse
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message
from dialogs.base_dialog import BaseDialog
from lib_telechatbot.bot_dispatcher import bot, applicant_bot, bot_dispatcher


class PublishDialog(BaseDialog):
    def __init__(self, from_user) -> None:
        super().__init__(DIALOGS['create_vacanse'], from_user)
        if MODE == 'publisher_ui':
            self.register_handlers()


    def register_handlers(self):
        vacanse_state = DIALOGS['create_vacanse']['state']

        bot_dispatcher.register_message_handler(
            callback=self.answer_callback,
            state=vacanse_state,
            content_types=['text'])

        bot_dispatcher.register_message_handler(
            callback=self.photo_callback,
            state=vacanse_state,
            content_types=['photo'])

    async def begin(self):
        await super().begin(),

    async def answer_callback(
            self, message: Message, state: FSMContext, *arrgs, **kwargs):
        await self.get_answer(message, state, self.finish)

    async def photo_callback(
            self, message: Message, state: FSMContext, *arrgs, **kwargs):
        file_id = message.photo[-1].file_id
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
        file: BytesIO = await bot.download_file_by_id(file_id)

        discriptions = data.get('discription')
        questions = data.get('questions')

        vacanse = Vacanse(
            photo=file_id,
            discriptions=discriptions,
            questions=questions,
            user_id=user_id)
        if file or discriptions or questions:
            vacanse.add()

        discription = vacanse.get_discription()

        # show_preview_to_publicher
        await message.answer_photo(photo=file_id, caption=vacanse,
                                   reply_markup=ReplyKeyboardRemove())

        # publishing to chanel
        await applicant_bot.send_photo(
            CHANEL_ID,
            photo=await bot.download_file_by_id(data.get('file_id')),
            caption=discription or '-',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    'Откликнуться', callback_data=f'respond {vacanse.id}')))

        state.finish()
