
from aiogram.dispatcher.filters.state import State
from messages import DIALOGS
from models import UserList, Vacanse
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message
from dialogs.base_dialog import BaseDialog
from lib_telechatbot.bot_dispatcher import bot_dispatcher


class PublishDialog(BaseDialog):
    def register_handlers(self):
        bot_dispatcher.register_message_handler(
            callback=self.answer_callback, state=DIALOGS['create_vacanse']['state'])

    async def begin(self, message: Message, state: FSMContext):
        await super().begin(message, state, 'create_vacanse')

    async def answer_callback(
            self, message: Message, state: FSMContext, *arrgs, **kwargs):
        await self.get_answer(message, state, self.finish)

    async def finish(self, message: Message, state: FSMContext):
        data = await state.get_data()
        user_id = await self.get_user_id(message, state)
        if not user_id:
            await message.answer('error',
                                 reply_markup=types.ReplyKeyboardRemove())
            return
        image=data.get('image')
        discriptions=data.get('discription')
        questions=data.get('questions')
        vacanse = Vacanse(image=image,
                          discriptions=discriptions,
                          questions=questions,
                          user_id=user_id)
        if image or discriptions or questions:
             vacanse.add()
        await message.answer(vacanse, reply_markup=types.ReplyKeyboardRemove())
        state.finish()



