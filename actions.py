from models.UserList import UserList
from models import Applicant
from models.Vacanse import Vacanse
from aiogram.types import ReplyKeyboardRemove, Message
from aiogram.dispatcher import FSMContext


async def list_published(message: Message, state: FSMContext):
    for vacanse in Vacanse.all():
        await message.answer(vacanse.id, reply_markup=ReplyKeyboardRemove())


async def publish(message: Message, state: FSMContext):
    user_id = UserList.all()[0].id
    Vacanse(user_id=user_id).add()
    # TODO run publication dialog


async def list_waiting_applicants(message: Message, state: FSMContext):
    for applicant in Applicant.all():
        await message.answer(applicant.id, reply_markup=ReplyKeyboardRemove())


async def show_stat(message: Message, state: FSMContext):
    ...


async def show_help(message: Message, state: FSMContext):
    from messages import MESSAGES
    await message.reply(
        MESSAGES['help'], reply_markup=ReplyKeyboardRemove())
