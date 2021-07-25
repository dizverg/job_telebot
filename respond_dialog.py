

from lib.dialog import Dialog
from aiogram.dispatcher.filters.state import State, StatesGroup
from attr import s
from config import CHANEL_ID, MODE
from io import BytesIO

from aiogram.types.callback_query import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from models import Vacanse
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message
from lib.base_dialog import BaseDialog
from lib.bot_dispatcher import bot, applicant_bot, bot_dispatcher


async def applicant_respond_callback(callback_query: CallbackQuery):
    vacanse_id = callback_query.data.split(' ')[1]

    await applicant_bot.answer_callback_query(
        callback_query.id, text=callback_query.data, show_alert=False)

    response_dialog = RespondDialog(
        config=Vacanse.find_by_id(vacanse_id).questions,
    )

    await response_dialog.begin(from_user=callback_query.from_user)

    # await bot.send_message(callback_query.from_user.id, callback_query.data)


class RespondDialog(BaseDialog):
    class RespondStatesGroup(StatesGroup):
            state = State()

    def __init__(self, config) -> None:
        super().__init__(applicant_bot, config)

        self.dialog_base_state = self.RespondStatesGroup.state

    async def begin(self, from_user):
        # await super().begin(from_user)
        await bot_dispatcher.storage.reset_data(user=from_user.id)
        await bot_dispatcher.storage.finish( user=from_user.id)
        await bot_dispatcher.storage.set_state(chat=from_user.id, user=from_user.id,
         state= self.dialog_base_state)


        if MODE == 'applicant_ui':
            bot_dispatcher.register_message_handler(
                callback=self.get_answer,
                state=self.dialog_base_state,
                content_types=['text'])

            bot_dispatcher.register_message_handler(
                callback=self.photo_callback,
                state=self.dialog_base_state,
                content_types=['photo'])

            bot_dispatcher.register_message_handler(
                callback=self.video_callback,
                state=self.dialog_base_state,
                content_types=['video'])

            # bot_dispatcher.register_message_handler(
            #     callback=self.get_answer2,
            #     state='*',
            #     # state=state,
            #     content_types=['text'])
        # await super().begin(from_user)

        dialog = Dialog(config=self.config, bot=self.bot)

        await self.dialog_base_state.set()
        state = bot_dispatcher.current_state(chat=from_user.id)
        await state.update_data({'dialog': dialog})
        await dialog.ask(from_user_id=from_user.id,
                              parameter_name=dialog.get_first())



    async def finish(self, message: Message, state: FSMContext):
        data = await state.get_data()
        # user_id = await self.get_user_id()
        # if not user_id:
        #     await message.answer('error',
        #                          reply_markup=ReplyKeyboardRemove())
        #     return

        # file_id = data.get('file_id')
        # if file_id:
        #     file: BytesIO = await bot.download_file_by_id(file_id)

        # discriptions = data.get('discription')

        await message.answer(data)

        # vacanse = Vacanse(
        #     photo=file_id,
        #     discriptions=discriptions,
        #     questions=questions,
        #     user_id=user_id)

        # if file_id or discriptions or questions:
        #     vacanse.add()

        # discription = vacanse.get_discription()
        # await message.answer()
        # # show_preview_to_publicher
        # await message.answer_video(video=file_id, caption=vacanse,
        #                            reply_markup=ReplyKeyboardRemove())

        # # publishing to chanel
        # await applicant_bot.send_video(
        #     CHANEL_ID,
        #     video=await bot.download_file_by_id(data.get('file_id')),
        #     caption=discription or '-',
        #     reply_markup=InlineKeyboardMarkup().add(
        #         InlineKeyboardButton(
        #             'Отклонить', callback_data=f'reject {vacanse.id}')))

        await super().finish(message, state)
