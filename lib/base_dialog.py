from abc import abstractclassmethod
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, ReplyKeyboardRemove

from models import UserList
from lib.bot_dispatcher import bot_dispatcher
from lib.dialog import Dialog


class DialogInterfase:

    @abstractclassmethod
    async def begin(cls, message: Message):
        ...

    @abstractclassmethod
    async def ask(cls, chat_id):
        ...

    @abstractclassmethod
    async def on_get_answer(cls, message: Message, state: FSMContext):
        ...


class BaseDialog(DialogInterfase):
    class States(StatesGroup):
        state = State()

    @classmethod
    async def begin(cls, message: Message, config):
        await cls.States.first()
        await cls.get_current_state().update_data({'config': config})
        await cls.ask(message.chat.id)

    @classmethod
    async def ask(cls, chat_id):
        current_question = await cls.current_question()
        loop_stop_word = current_question.get('loop_stop_word')

        if loop_stop_word:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(loop_stop_word)
        else:
            keyboard = ReplyKeyboardRemove()

        await bot_dispatcher.bot.send_message(
            chat_id, current_question.get('text'), reply_markup=keyboard)

    @classmethod
    async def get_answer(cls, message: Message, state: FSMContext):
        await cls.dialog.get_answer(message, state, cls.finish)

    @classmethod
    def get_current_state(cls):
        return bot_dispatcher.current_state()

    @classmethod
    async def get_field_from_state(cls):
        return str(await cls.get_current_state().get_state()).split(':')[1]

    @classmethod
    async def current_question_text(cls):
        return (await cls.current_question()).get('text')

    @classmethod
    async def current_question(cls) -> dict:
        return (await cls.get_config()).get('questions').get(
            await cls.get_field_from_state())

    @classmethod
    async def get_config(cls):
        return (await cls.get_current_state().get_data()).get('config')

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

        user = await UserList.get_user(user_telegram_id=from_user.id)

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
