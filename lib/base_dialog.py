from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from models import UserList
from lib.bot_dispatcher import bot_dispatcher
from lib.dialog import Dialog


class BaseDialog:
    def __init__(self, bot, config) -> None:
        super().__init__()
        self.user = None
        self.config = config
        self.bot = bot
        class states_group(StatesGroup):
            state = State()
        self.dialog_base_state = states_group.state
        self.dialog = Dialog(self.config, self.bot)
    # def register_handlers(self, state):
    #     bot_dispatcher.register_message_handler(
    #         callback=self.get_answer,
    #         state=state,
    #         content_types=['text'])


    #     bot_dispatcher.register_message_handler(
    #         callback=self.photo_callback,
    #         state=state,
    #         content_types=['photo'])

    #     bot_dispatcher.register_message_handler(
    #         callback=self.video_callback,
    #         state=state,
    #         content_types=['video'])

        # bot_dispatcher.register_message_handler(
        #     callback=self.get_answer2,
        #     state='*',
        #     # state=state,
        #     content_types=['text'])


    async def begin(self, from_user):
        

        await self.dialog_base_state.set()
        await self.dialog.ask(from_user_id=from_user.id,
                              parameter_name=self.dialog.get_first())

    async def finish_dialog(self, message: Message, state: FSMContext):
        await message.answer(str(await state.get_data()),
                             reply_markup=(types.ReplyKeyboardRemove()))

    async def get_answer(self, message: Message, state: FSMContext):
        # dialog = await self.get_dialog(message.from_user)
        await self.dialog.get_answer(message, state, self.finish)

    # async def get_answer2(self, message: Message, state: FSMContext):
    #     await self.dialog.get_answer(message, state, self.finish)

    async def photo_callback(
            self, message: Message, state: FSMContext):
        file_id = message.photo[-1].file_id
        await state.update_data({'file_id': file_id})
        await self.get_answer(message, state)

    async def video_callback(
            self, message: Message, state: FSMContext, *arrgs, **kwargs):
        file_id = message.video[-1].file_id
        await state.update_data({'file_id': file_id})
        await self.get_answer(message, state, self.finish)

    async def finish(self, message: Message, state: FSMContext):
        await state.finish()


class AuthMixin:

    async def auth(from_user):
        if not from_user:
            return

        user = await UserList.get_user( user_telegram_id=from_user.id)

        # excess_fields = {'dialog', 'current_field', 'loop_stop_word', 'user'}
        # data = dict((k, v) for k, v in data.items() if k not in excess_fields)

        new_data = {
            'telegram_id': from_user.id,
            'username': from_user.username,
            'is_bot': from_user.is_bot,
            'language_code': from_user.language_code,
            'first_name': from_user.first_name}

        if user:
            user.update(user.id, new_data)
        else:
            user = UserList(**new_data)
            user.add()
        return user

    @classmethod
    async def get_user_id(cls, from_user):
        user = await cls.auth(from_user)
        return user.id if user else None
