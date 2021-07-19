
from lib_telechatbot.bot_dispatcher import bot_dispatcher

from models.UserList import UserList
from models import Applicant
from models.Vacanse import Vacanse
from aiogram.types import ReplyKeyboardRemove, Message
from aiogram.dispatcher import FSMContext

def register_main_menu_handlers():
    from messages import MAIN_MENU
    for key, value in MAIN_MENU.items():
        bot_dispatcher.register_message_handler(
            value.get("action",None), commands=key)

async def list_published(message: Message, state: FSMContext):
    for vacanse in Vacanse.all():
        await message.answer(vacanse, reply_markup=ReplyKeyboardRemove())


async def publish(message: Message, state: FSMContext):
    # Vacanse(user_id=user_id).add()
    from dialogs.publush_dialog import PublishDialog
    await PublishDialog().begin(message, state)
    # TODO run publication dialog


async def list_waiting_applicants(message: Message, state: FSMContext):
    for applicant in Applicant.filter_by(accepted=None).all():
        await message.answer(applicant, reply_markup=ReplyKeyboardRemove())


async def show_stat(message: Message, state: FSMContext):
    waiting_count = Applicant.filter_by(accepted=None).count()
    accepted_count = Applicant.filter_by(accepted=True).count()
    rejected_count = Applicant.filter_by(accepted=False).count()
    await message.answer(
        f"Одобрено: {accepted_count}\n"
        f"Отклонено: {rejected_count}\n"
        f"В ожидании: {waiting_count}\n",
        reply_markup=ReplyKeyboardRemove())


async def show_help(message: Message, state: FSMContext):
    from messages import MESSAGES
    await message.reply(MESSAGES['help'], reply_markup=ReplyKeyboardRemove())
