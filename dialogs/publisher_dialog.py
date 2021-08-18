from io import BytesIO
from aiogram.types.inline_keyboard import InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

from cfg.config import CHANNEL_ID
from cfg.messages import MESSAGES
from lib.base_dialog import AuthMixin, BaseDialog
from lib.bot_dispatcher import bot_dispatcher, applicant_bot
from models import Vacancy

publisher_dialog_cfg = {
    'questions': {
        'photo': {
            'text': 'Фото',
            'type': 'photo',
        },
        'description': {
            'text': 'Опишите вакансию',
            'loop_stop_word': 'Закончить с описанием',
        },
        'questions': {
            'text': 'Задайте вопрос соискателю',
            'loop_stop_word': 'Достаточно вопросов'
        }
    },
    'order': ['description', 'questions', 'photo', ]
}


class PublisherDialog(BaseDialog, AuthMixin):
    class States(StatesGroup):
        description = State()
        questions = State()
        photo = State()

    @classmethod
    async def begin(cls, chat_id):
        await super().begin(chat_id, publisher_dialog_cfg)

    @classmethod
    async def get_text_answer(cls, message: Message, state: FSMContext):
        chat_id = message.chat.id
        text = message.text
        data = await state.get_data()
        field = await cls.get_field_from_state(chat_id)

        loop_stop_word = (await cls.current_question(chat_id)
                          ).get('loop_stop_word')

        if text != loop_stop_word:
            new_data = data.get(field, []) + [text]
            await state.update_data({field: new_data})

        if not loop_stop_word or text == loop_stop_word:
            await cls.States.next()

        # await cls.ask(message.chat.id)

        question_number = data.get('question_number', 0)
        max_number = len(data.get('config', dict()).get('order')) - 1
        if question_number < max_number:
            new_number = data.get('question_number', 0) + (
                1 if not loop_stop_word or text == loop_stop_word else 0)
            await cls.ask(chat_id, new_number)
        else:
            await cls.on_finish(message, state)

    @staticmethod
    async def get_photo_answer(message: Message, state: FSMContext):
        file_id = message.photo[-1].file_id

        data = await state.get_data()

        await state.finish()

        user_id = AuthMixin.get_user_id(message.from_user)
        if not user_id:
            await message.answer('error', reply_markup=ReplyKeyboardRemove())
            return

        # file: BytesIO = await message.bot.download_file_by_id(file_id)

        descriptions = data.get('description')
        questions = data.get('questions')

        vacancy = Vacancy(photo=file_id, descriptions=descriptions,
                          questions=questions, user_id=user_id)

        if file_id or descriptions or questions:
            vacancy.add()

        # show_preview_to_publisher
        await message.answer_photo(photo=file_id, caption=vacancy,
                                   reply_markup=ReplyKeyboardRemove())

        # publishing to channel
        await applicant_bot.send_photo(
            CHANNEL_ID,
            photo=await message.bot.download_file_by_id(file_id),
            caption=vacancy.get_description() or '-',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    MESSAGES['go_to_bot'],
                    url=f'https://t.me/jober_bober_bot?start={vacancy.id}')))
