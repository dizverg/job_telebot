from io import BytesIO

from aiogram.types.callback_query import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from config import CHANEL_ID
from messages import DIALOGS
from models import Vacanse
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message
from dialogs.base_dialog import BaseDialog
from lib_telechatbot.bot_dispatcher import bot, bot_dispatcher


class PublishDialog(BaseDialog):

    def register_handlers(self):
        vacanse_state = DIALOGS['create_vacanse']['state']
        bot_dispatcher.register_message_handler(
            callback=self.answer_callback, state=vacanse_state, content_types=['text'])

        bot_dispatcher.register_message_handler(
            callback=self.photo_callback, state=vacanse_state, content_types=['photo'])

        # bot_dispatcher.register_message_handler(
        #     callback=self.photo_callback, state=vacanse_state)

    async def begin(self, message: Message, state: FSMContext):
        await super().begin(message, state, 'create_vacanse')

    async def answer_callback(
            self, message: Message, state: FSMContext, *arrgs, **kwargs):
        await self.get_answer(message, state, self.finish)

    async def photo_callback(
            self, message: Message, state: FSMContext, *arrgs, **kwargs):
        photo = message.photo[-1]
        await state.update_data({'file_id': photo.file_id})

        # await bot.send_photo(CHANEL_ID, photo=file_id)

        # await bot.send_message(CHANEL_ID, 'photo=message.photo[-1]')
        await self.get_answer(message, state, self.finish)

    async def finish(self, message: Message, state: FSMContext):
        data = await state.get_data()
        user_id = await self.get_user_id(message, state)
        if not user_id:
            await message.answer('error',
                                 reply_markup=types.ReplyKeyboardRemove())
            return
        photo = data.get('file_id')
        discriptions = data.get('discription')
        questions = data.get('questions')
        vacanse = Vacanse(photo=photo,
                          discriptions=discriptions,
                          questions=questions,
                          user_id=user_id)
        if photo or discriptions or questions:
            vacanse.add()

        inline_btn_1 = InlineKeyboardButton(
            'Откликнуться', callback_data=vacanse.id)
        inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

        bot_dispatcher.register_callback_query_handler(
            self.process_callback_vacanse)

        await bot.send_photo(CHANEL_ID, photo=photo, caption=vacanse.get_discription(),
                             reply_markup=inline_kb1)

        await message.answer_photo(photo=photo, caption=vacanse, reply_markup=types.ReplyKeyboardRemove())
        # await message.answer(vacanse, reply_markup=types.ReplyKeyboardRemove())
        state.finish()

    async def process_callback_vacanse(self, callback_query: CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Тут анкета будет')
