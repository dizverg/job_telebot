

from io import BytesIO

from aiogram.dispatcher.filters.state import State, StatesGroup
from lib_telechatbot.dialog import Dialog
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from sqlalchemy.sql.expression import text
from config import CHANEL_ID, MODE

from models import Vacanse
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message
from dialogs.base_dialog import BaseDialog
from lib_telechatbot.bot_dispatcher import bot, applicant_bot, bot_dispatcher


create_vacanse_dialog_config = {
    'questions': {
        'photo': {
            'text': 'Фото',
            'type': 'photo',
        },
        'discription': {
            'text': 'Опишите вакансию',
            'loop_stop_word': 'Закончить с описанием',
        },
        'questions': {
            'text': 'Задайте вопрос соискателю',
            'loop_stop_word': 'Достаточно вопросов'
        }
    },
    'order': ['discription', 'questions','photo', ]
}


class pub(StatesGroup):
    st = State()


    
class PublishDialog(BaseDialog):
    def __init__(self) -> None:
        self.dialog_config =create_vacanse_dialog_config

        super().__init__(self.dialog_config)
        if MODE == 'publisher_ui':
            self.register_handlers()


    def register_handlers(self):
        bot_dispatcher.register_message_handler(
            callback=self.answer_callback,
            state=pub.st,
            content_types=['text'])

        bot_dispatcher.register_message_handler(
            callback=self.photo_callback,
            state=pub.st,
            content_types=['photo'])

    async def begin(self,from_user, state):
        await pub.st.set()
        # await super().begin(from_user)
        self.user = await self.auth(from_user)

        await self.dialog.ask(from_user_id=from_user.id,
                              parameter_name=self.dialog.get_first(), 
                        )


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
        user_id = await self.get_user_id(message.from_user)
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


publish_dialog = PublishDialog()