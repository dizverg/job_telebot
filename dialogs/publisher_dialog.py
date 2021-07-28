from io import BytesIO
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, ReplyKeyboardRemove

from cfg.config import CHANEL_ID
from lib.base_dialog import AuthMixin
from lib.bot_dispatcher import bot_dispatcher, applicant_bot
from models import Vacanse


publisher_dialog_cfg = {
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
    'order': ['discription', 'questions', 'photo', ]
}


class PublisherDialog(AuthMixin):
    class States(StatesGroup):
        discription = State()
        questions = State()
        photo = State()    

    @classmethod
    async def begin(cls, message: Message):
        await cls.States.first()
        await cls.ask(message.chat.id)

    @classmethod
    async def ask(cls, chat_id):
        current_question = await cls.current_question()
        loop_stop_word = current_question.get('loop_stop_word')

        if loop_stop_word:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(loop_stop_word)
        else:
            keyboard = ReplyKeyboardRemove()

        await bot_dispatcher.bot.send_message(
            chat_id, current_question.get('text'), reply_markup=keyboard)

    @staticmethod
    async def get_field_from_state():
        return str(await bot_dispatcher.current_state().get_state()).split(':')[1]

    @classmethod
    async def current_question_text(cls):
        return (await cls.current_question()).get('text')

    @classmethod
    async def current_question(cls) -> dict:
        return publisher_dialog_cfg.get('questions').get(
            await cls.get_field_from_state())

    @classmethod
    async def get_text_answer(cls, message: Message, state: FSMContext):
        text = message.text
        data = await state.get_data()
        field = await cls.get_field_from_state()

        loop_stop_word = (await cls.current_question()
                          ).get('loop_stop_word')

        if text != loop_stop_word:
            new_data = data.get(field, []) + [text]
            await state.update_data({field: new_data})

        if not loop_stop_word or text == loop_stop_word:
            await cls.States.next()

        await cls.ask(message.chat.id)

    @staticmethod
    async def get_photo_answer(message: Message, state: FSMContext):
        file_id = message.photo[-1].file_id

        data = await state.get_data()

        await state.finish()

        user_id = await AuthMixin.get_user_id(message.from_user)
        if not user_id:
            await message.answer('error', reply_markup=ReplyKeyboardRemove())
            return

        file: BytesIO = await message.bot.download_file_by_id(file_id)

        discriptions = data.get('discription')
        questions = data.get('questions')

        vacanse = Vacanse(photo=file_id, discriptions=discriptions,
                          questions=questions,  user_id=user_id)

        if file or discriptions or questions:
            vacanse.add()

        # show_preview_to_publicher
        await message.answer_photo(photo=file_id, caption=vacanse,
                                   reply_markup=ReplyKeyboardRemove())

        # publishing to chanel
        from cfg.messages import MESSAGES
        await applicant_bot.send_photo(
            CHANEL_ID,
            photo=await message.bot.download_file_by_id(file_id),
            caption=vacanse.get_discription() or '-',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(MESSAGES['response'], callback_data=f'applicant_ui {vacanse.id}')))
