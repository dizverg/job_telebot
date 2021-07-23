from io import BytesIO
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message

from config import CHANEL_ID, MODE
from models import Vacanse
from dialogs.base_dialog import AuthMixin, BaseDialog
from lib_telechatbot.bot_dispatcher import bot, applicant_bot, bot_dispatcher, publisher_bot


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
    'order': ['discription', 'questions', 'photo', ]
}


class PublishDialog(BaseDialog, AuthMixin):
    def __init__(self) -> None:
        super().__init__(publisher_bot, create_vacanse_dialog_config)

        if MODE == 'publisher_ui':
            bot_dispatcher.register_message_handler(
                callback=self.get_answer,
                state=self.dialog_base_state,
                content_types=['text'])

            bot_dispatcher.register_message_handler(
                callback=self.photo_callback,
                state=self.dialog_base_state,
                content_types=['photo'])

    async def begin(self, from_user, state: FSMContext):
        await super().begin(from_user, state)
        self.user = await self.auth(from_user)

    async def finish(self, message: Message, state: FSMContext):
        data = await state.get_data()
        user_id = await self.get_user_id(message.from_user)
        if not user_id:
            await message.answer('error', reply_markup=ReplyKeyboardRemove())
            return

        file_id = data.get('file_id')
        file: BytesIO = await bot.download_file_by_id(file_id)

        discriptions = data.get('discription')
        questions = data.get('questions')

        vacanse = Vacanse(photo=file_id, discriptions=discriptions,
                          questions=questions,  user_id=user_id)

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

        super().finish(message, state)


publish_dialog = PublishDialog()
