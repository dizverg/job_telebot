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
    async def ask(cls, chat_id, question_number):
        ...

    @abstractclassmethod
    async def on_get_answer(cls, message: Message, state: FSMContext):
        ...


class BaseDialog(DialogInterfase):
    class States(StatesGroup):
        state = State()

    @classmethod
    async def begin(cls, chat_id: int, config, **kwargs):
        if type(config) == list:
            config = {
                'questions': {v: {'text': v, 'type': '*'} for v in config},
                'order': config}


        state = cls.get_current_state(chat_id)
        await state.set_state(cls.States.state)

        await state.update_data({
            'config': config,
            'chat_id': chat_id,
            **kwargs
        })
        await cls.ask(chat_id, 0)

    @classmethod
    async def ask(cls, chat_id, question_number):
        state = cls.get_current_state(chat_id)
        await state.update_data({'question_number': question_number})

        current_question = await cls.current_question(chat_id)

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
        data = await state.get_data()
        question_number = data.get('question_number')
        current_question = await cls.current_question(message.chat.id)

        # check_result = await self.check_answer(
        #     self.get_parameter_by_name(field_name), message)

        # if not check_result:
        #     await self.ask(
        #         from_user_id=message.from_user.id,
        #         parameter_name=field_name)
        #     return

        # field_value = (field_value if type(field_value) == list
        #                else [field_value] if field_value else [])

        # loop_stop_word = data.get('loop_stop_word')
        # # if not loop_stop_word or loop_stop_word == answer:

        # if message.photo:
        #     await state.update_data({field_name + '_photo': message.photo[-1]})

        # if message.video:
        #     await state.update_data({field_name + '_video': message.video[-1]})

        # if loop_stop_word != text:
        #     await state.update_data({field_name: field_value + [text]})

        # next_field = (field_name if loop_stop_word and loop_stop_word != text
        #               else self.get_next(field_name))

        # if next_field:
        #     # print(str(await state.get_data()))
        #     await self.ask(
        #         from_user_id=message.from_user.id,
        #         parameter_name=next_field)
        # else:
        #     await state.update_data({'current_field': None})
        #     await on_finish(message=message, state=state)
        #     await state.finish()

        # await cls.dialog.get_answer(message, state, cls.finish)

    @classmethod
    def get_current_state(cls, chat_id):
        return bot_dispatcher.current_state(chat=chat_id)

    @classmethod
    async def get_field_from_state(cls, chat_id):
        return str(await cls.get_current_state(chat_id).get_state()).split(':')[1]

    @classmethod
    async def current_question_text(cls,chat_id):
        return (await cls.current_question(chat_id)).get('text')

    @classmethod
    async def get_data_from_state(cls, chat_id):
        state = cls.get_current_state(chat_id)
        return await state.get_data()
        

    @classmethod
    async def current_question(cls, chat_id) -> dict:
        config = await cls.get_config(chat_id)
        questions = config.get('questions')

        data = await cls.get_data_from_state(chat_id)
        question_number = data.get('question_number', 0)
        question = config.get('order')[question_number]

        return questions.get(question)

    @classmethod
    async def get_config(cls, chat_id):
        data = await cls.get_data_from_state(chat_id)
        return data.get('config')

    # async def finish_dialog(self, message: Message, state: FSMContext):
    #     await message.answer(str(await state.get_data()),
    #                          reply_markup=(types.ReplyKeyboardRemove()))

    # async def get_answer(self, message: Message, state: FSMContext):
    #     # dialog = await self.get_dialog(message.from_user)
    #     await self.dialog.get_answer(message, state, self.finish)

    # # async def get_answer2(self, message: Message, state: FSMContext):
    #     await self.dialog.get_answer(message, state, self.finish)

    # async def photo_callback(
    #         self, message: Message, state: FSMContext):
    #     file_id = message.photo[-1].file_id
    #     await state.update_data({'file_id': file_id})
    #     await self.get_answer(message, state)

    # async def video_callback(
    #         self, message: Message, state: FSMContext, *arrgs, **kwargs):
    #     file_id = message.video[-1].file_id
    #     await state.update_data({'file_id': file_id})
    #     await self.get_answer(message, state, self.finish)

    @classmethod
    async def on_finish(cls, message: Message, state: FSMContext):
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
