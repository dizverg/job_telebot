from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.mixins import DataMixin
from lib_telechatbot.dialog import Dialog

from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.types import ContentTypes, Message
from aiogram.utils import executor


from models import UserList

from lib_telechatbot.bot_dispatcher import bot


class BaseDialog:
    def __init__(self, bot, config) -> None:
        super().__init__()
        self.user = None
        self.config = config
        self.bot = bot
        self.dialog = Dialog(config=self.config, bot=self.bot)

        class states_group(StatesGroup):
            state = State()
        self.dialog_base_state = states_group.state

    async def begin(self, from_user, state: FSMContext):
        await self.dialog_base_state.set()
        await self.dialog.ask(from_user_id=from_user.id,
                              parameter_name=self.dialog.get_first(),
                              state=state)

    async def finish_dialog(self, message: Message, state: FSMContext):
        await message.answer(str(await state.get_data()),
                             reply_markup=(types.ReplyKeyboardRemove()))

    async def get_answer(self, message: Message, state: FSMContext):
        await self.dialog.get_answer(message, state, self.finish)

    async def photo_callback(
            self, message: Message, state: FSMContext):
        file_id = message.photo[-1].file_id
        await state.update_data({'file_id': file_id})
        await self.get_answer(message, state)

    async def finish(self, message: Message, state: FSMContext):
        state.finish()


class AuthMixin:
    async def auth(self, from_user):
        if not from_user:
            return

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
            return self.user
        else:
            return

    async def get_user_id(self, from_user):
        user = await self.auth(from_user)
        return user.id if user else None
