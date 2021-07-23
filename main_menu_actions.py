from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.types.inline_keyboard import (InlineKeyboardButton,
                                           InlineKeyboardMarkup)
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup

from models import Applicant

from models.Vacanse import Vacanse
from register_handlers import publish_dialog


async def list_published(message: Message, state: FSMContext):
    for vacanse in Vacanse.all():
        await message.answer_photo(photo=vacanse.photo,
                                   caption=vacanse.get_discription(),
                                   reply_markup=ReplyKeyboardRemove())
        # await message.answer(vacanse, reply_markup=ReplyKeyboardRemove())


async def publish(message: Message, state: FSMContext):
    # Vacanse(user_id=user_id).add()
    
    await publish_dialog.begin()
   

async def list_waiting_applicants(message: Message, state: FSMContext):
    for applicant in Applicant.filter_by(accepted=None).all():
        await message.answer(applicant, reply_markup=ReplyKeyboardRemove())


async def show_stat(message: Message, state: FSMContext):
    markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Отправить свой контакт ☎️', request_contact=True))


    vacanse_count = Vacanse.query().count()
    waiting_count = Applicant.filter_by(accepted=None).count()
    accepted_count = Applicant.filter_by(accepted=True).count()
    rejected_count = Applicant.filter_by(accepted=False).count()
    await message.answer(
        f"Опубликовано вакансий: {vacanse_count}\n"
        f"Одобрено: {accepted_count}\n"
        f"Отклонено: {rejected_count}\n"
        f"В ожидании: {waiting_count}\n",
        # reply_markup=inline_kb1
        reply_markup=ReplyKeyboardRemove()
    )


async def show_help(message: Message, state: FSMContext):
    from messages import MESSAGES
    await message.reply(MESSAGES['help'], reply_markup=ReplyKeyboardRemove())
