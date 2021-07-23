from aiogram.dispatcher.filters.state import State
from aiogram.utils.mixins import DataMixin
from lib_telechatbot.dialog import Dialog

from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.types import ContentTypes, Message
from aiogram.utils import executor


from models import UserList

from lib_telechatbot.bot_dispatcher import bot_dispatcher, bot


class BaseDialog:
    command: str
    user = None
    dialog: Dialog


    def __init__(self, config) -> None:
        super().__init__()
        self.config = config
        self.state = State()
        self.from_user = None
        self.dialog = Dialog(config=self.config, bot=bot)

    async def begin(self, from_user):
        self.from_user = from_user
        self.user = await self.auth()

        # await self.state.update_data({'dialog': self.dialog})

        await self.dialog.ask(from_user_id=self.from_user.id,
                              parameter_name=self.dialog.get_first())

    async def auth(self):
        # data = await state.get_data()
        self.user = self.user or await UserList.get_user(
            user_telegram_id=self.from_user.id)

        # excess_fields = {'dialog', 'current_field', 'loop_stop_word', 'user'}
        # data = dict((k, v) for k, v in data.items() if k not in excess_fields)

        new_data = {
            'telegram_id': self.from_user.id,
            'username': self.from_user.username,
            'is_bot': self.from_user.is_bot,
            'language_code': self.from_user.language_code,
            'first_name': self.from_user.first_name}
        if self.user:
            self.user.update(self.user.id, new_data)
        else:
            self.user = UserList(**new_data)
            self.user.add()

        if self.user:
            # await self.state.update_data({'user': self.user})
            return self.user
        else:
            return

    async def get_user_id(self):
        user = await self.auth()
        return user.id if user else None

    async def finish_dialog(self, message: Message, state: FSMContext,
                            *args, **kwargs):
        await message.answer(str(await state.get_data()),
                             reply_markup=(types.ReplyKeyboardRemove()))

    async def get_answer(
            self, message: Message, state: FSMContext, on_finish=None):
        # try:

        if self.dialog:
            await self.dialog.get_answer(message, state, on_finish)
        # except:
        ...

    async def finish(self, message: Message, state: FSMContext):

        from messages import MESSAGES

        await message.answer(MESSAGES.get('data_saved', '{}'),
                             reply_markup=types.ReplyKeyboardRemove())
