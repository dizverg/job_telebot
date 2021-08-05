from io import BytesIO
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, ReplyKeyboardRemove

from cfg.config import CHANEL_ID, HR_ID
from lib.base_dialog import AuthMixin, BaseDialog
from lib.bot_dispatcher import bot_dispatcher, applicant_bot, hr_bot
from models import Applicant, Vacanse


class RespondDialog(BaseDialog, AuthMixin):
    @classmethod
    async def begin(cls, chat_id: int, config, vacanse_id):
        await super().begin(chat_id, config, vacanse_id=vacanse_id)

    @classmethod
    async def get_text_answer(cls, message: Message, state: FSMContext):
        # state = cls.get_current_state(message.ch)
        chat_id = message.chat.id

        data = await state.get_data()

        field = await cls.current_question_text(chat_id)

        loop_stop_word = (await cls.current_question(chat_id)
                          ).get('loop_stop_word')

        text = message.text

        if text != loop_stop_word:
            new_data = data.get(field, []) + [text]
            await state.update_data({field: new_data})

        question_number = data.get('question_number', 0)
        if not loop_stop_word or text == loop_stop_word:
            if len(cls.States.states) > 1:
                await cls.States.next()
            question_number += 1

        if question_number < len(data.get('config', dict()).get('order')):
            await cls.ask(chat_id, question_number)
        else:
            await cls.on_finish(message, state)

    @staticmethod
    async def get_video_answer(message: Message, state: FSMContext):
        file_id = message.video.file_id

        data = await state.get_data()

        await state.finish()

        user_id = await AuthMixin.get_user_id(message.from_user)
        if not user_id:
            await message.answer('error', reply_markup=ReplyKeyboardRemove())
            return

        file: BytesIO = await message.bot.download_file_by_id(file_id)

        # discriptions = data.get('discription')
        # questions = data.get('questions')

        applicant = Applicant(video=file_id, json=data, user_id=user_id)

        applicant.add()

        await message.answer_video(video=file_id, caption=data,
                                   reply_markup=ReplyKeyboardRemove())

        # TODO show_to_HR
        from cfg.messages import MESSAGES
        await hr_bot.send_video(
            HR_ID,
            video=await message.bot.download_file_by_id(file_id),
            caption=data,
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    MESSAGES['accept'], 
                    callback_data=f'{applicant.id}'),
                InlineKeyboardButton(
                    MESSAGES['reject'], 
                    callback_data=f'{applicant.id}')
            )
        )


    
