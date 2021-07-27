from io import BytesIO
from lib.dialog import Dialog
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.message import Message

from config import CHANEL_ID, MODE
from models import Vacanse
from lib.base_dialog import AuthMixin, BaseDialog
from lib.bot_dispatcher import bot, applicant_bot, publisher_bot, bot_dispatcher


class PublishDialog(BaseDialog, AuthMixin):
    def __init__(self) -> None:
        # super().__init__(publisher_bot, create_vacanse_dialog_config)
        self.user = None
        self.config = create_vacanse_dialog_config
        self.bot = bot
        class PublishStatesGroup(StatesGroup):
            state = State()
        self.dialog_base_state = PublishStatesGroup.state


    async def begin(self, from_user, state: FSMContext):
        self.dialog = Dialog(config=self.config, bot=self.bot)
        
        await self.dialog_base_state.set()
        if MODE == 'publisher_ui':            
            bot_dispatcher.register_message_handler(
                callback=self.get_answer,
                state=self.dialog_base_state,
                content_types=['text'])


            bot_dispatcher.register_message_handler(
                callback=self.photo_callback,
                state=self.dialog_base_state,
                content_types=['photo'])

        await super().begin(from_user)

        self.user = await self.auth(from_user)

    async def finish(self, message: Message, state: FSMContext):
        data = await state.get_data()
        user_id = await self.get_user_id(message.from_user)
        if not user_id:
            await message.answer('error', reply_markup=ReplyKeyboardRemove())
            return

        file_id = data.get('file_id')
        file: BytesIO = await bot.download_file_by_id(file_id)

        discriptions = data.get('discription')
        questions = data.get('questions')

        vacanse = Vacanse(photo=file_id, discriptions=discriptions,
                          questions=questions,  user_id=user_id)

        if file or discriptions or questions:
            vacanse.add()

        # show_preview_to_publicher
        await message.answer_photo(photo=file_id, caption=vacanse,
                                   reply_markup=ReplyKeyboardRemove())

        from messages import MESSAGES
        # publishing to chanel
        await applicant_bot.send_photo(
            CHANEL_ID,
            photo=await bot.download_file_by_id(data.get('file_id')),
            caption=vacanse.get_discription() or '-',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(MESSAGES['response'], callback_data=f'applicant_ui {vacanse.id}')))

        super().finish(message, state)



