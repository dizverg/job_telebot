from lib_telechatbot.dialog import Dialog

from aiogram import types
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
        user = (await state.get_data()).get(
            'user', await UserList.get_user(message.from_user.id))
        if user:
            await state.update_data({'user': user})
            return user
        else:
            return

    async def finish_dialog(self, message: Message, state: FSMContext,
                            *args, **kwargs):
        await message.answer(str(await state.get_data()),
                             reply_markup=(types.ReplyKeyboardRemove()))

    async def get_answer(
        self, message: Message, state: FSMContext, on_finish=None):
        try:
            await ((await state.get_data()
                    ).get('dialog')).get_answer(message, state, on_finish)
        except:
            ...
