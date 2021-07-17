
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
        from_user = message.from_user

        if data.get('user'):
            user = data.pop('user')
        else:
            user = None

        if data.get('loop_stop_word'):
            data.pop('loop_stop_word')

        data.pop('dialog')
        data.pop('current_field')
        new_data = {'json': data,
                    'telegram_id': from_user.id,
                    'username': from_user.username,
                    'is_bot': from_user.is_bot,
                    'language_code': from_user.language_code,
                    'first_name': from_user.first_name}
        if user:
            user.update(new_data)
        else:
            user = UserList(**new_data).add()

        Vacanse(image=data.get('image'),
                discriptions=data.get('discription'), 
                questions=data.get('questions'), 
                user_id=user.id).add()

        # await message.reply(state)
        from messages import MESSAGES

        await message.answer(str(MESSAGES.get('data_saved', '{}')).format(data),
                             reply_markup=types.ReplyKeyboardRemove())
