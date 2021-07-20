from aiogram.utils.mixins import DataMixin
from lib_telechatbot.dialog import Dialog

from aiogram import bot, types
from aiogram.dispatcher import FSMContext, filters
from aiogram.types import ContentTypes, Message
from aiogram.utils import executor


from models import UserList

from lib_telechatbot.bot_dispatcher import bot_dispatcher as dp


class BaseDialog:

    command: str
    user = None
    dialog: Dialog

    async def begin(self, message: Message, state: FSMContext, command: str):
        self.command = command
        self.user = await self.auth(message, state)
        from messages import DIALOGS
        self.dialog = Dialog(config=DIALOGS[command])
        await state.update_data({'dialog': self.dialog})
        await self.dialog.ask(message=message,
                              parameter_name=self.dialog.get_first())

    async def auth(self, message: Message, state: FSMContext):
        from_user = message.from_user
        # data = await state.get_data()
        self.user = self.user or await UserList.get_user(
            user_telegram_id=from_user.id)

        # excess_fields = {'dialog', 'current_field', 'loop_stop_word', 'user'}
        # data = dict((k, v) for k, v in data.items() if k not in excess_fields)

        new_data = {
                    'telegram_id': from_user.id,
                    'username': from_user.username,
                    'is_bot': from_user.is_bot,
                    'language_code': from_user.language_code,
                    'first_name': from_user.first_name}
        if self.user:
            self.user.update(self.user.id, new_data)
        else:
            self.user = UserList(**new_data)
            self.user.add()

        if self.user:
            await state.update_data({'user': self.user})
            return self.user
        else:
            return

    async def get_user_id(self, message: Message, state: FSMContext):
        user = await self.auth(message, state)
        return user.id if user else None

    async def finish_dialog(self, message: Message, state: FSMContext,
                            *args, **kwargs):
        await message.answer(str(await state.get_data()),
                             reply_markup=(types.ReplyKeyboardRemove()))

    async def get_answer(
            self, message: Message, state: FSMContext, on_finish=None):
        # try:
            dialog: Dialog = (await state.get_data()).get('dialog')
            if dialog:
                await dialog.get_answer(message, state, on_finish)
        # except:
            ...

    async def finish(self, message: Message, state: FSMContext):

        from messages import MESSAGES

        await message.answer(MESSAGES.get('data_saved', '{}'),
                             reply_markup=types.ReplyKeyboardRemove())

