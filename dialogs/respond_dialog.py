from io import BytesIO
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, ReplyKeyboardRemove

from cfg.config import CHANEL_ID
from lib.base_dialog import AuthMixin, BaseDialog
from lib.bot_dispatcher import bot_dispatcher, applicant_bot
from models import Vacanse



class RespondDialog(BaseDialog, AuthMixin):
    @classmethod
    async def begin(cls, chat_id: int, config, vacanse_id):
        await super().begin(chat_id, config, vacanse_id=vacanse_id)


    @classmethod
    async def get_text_answer(cls, message: Message, state: FSMContext):
        state = cls.get_current_state()
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
