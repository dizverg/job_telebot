from cfg.messages import MESSAGES
from cfg.config import CHANEL_ID
from lib.dialog import Dialog
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.types.inline_keyboard import (InlineKeyboardButton,
                                           InlineKeyboardMarkup)
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup

from dialogs.publush_dialog import PublishDialog

from models import Applicant
from models import Vacanse
from lib.bot_dispatcher import applicant_bot


async def publish(message: Message, state: FSMContext):
    data = await Dialog.ask(config, state)
    if not data:
        return
    vacanse = Vacanse(**data)
    vacanse.add()

    await message.answer_photo(photo=data.get('file_id'), caption=vacanse,
                                   reply_markup=ReplyKeyboardRemove())
    
    await applicant_bot.send_photo(
            CHANEL_ID,
            photo=await message.bot.download_file_by_id(data.get('file_id')),
            caption=vacanse.get_discription() or '-',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(MESSAGES['response'], callback_data=f'applicant_ui {vacanse.id}')))


    await PublishDialog.begin(message.from_user, state)


async def list_published(message: Message, state: FSMContext):
    for vacanse in Vacanse.all():
        await message.answer_photo(photo=vacanse.photo,
                                   caption=vacanse,
                                   reply_markup=ReplyKeyboardRemove())


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


PUBLISHER_MENU = {
    'published': {'title': 'Просмотреть публикованные вакансии', 'action': list_published},
    'publish': {'title': 'Опубликовать вакансию', 'action': publish},
    'applicants': {'title': 'Соискатили в ожидании ответа', 'action': list_waiting_applicants},
}

DEFAULT_MENU = {
    'stat': {'title': 'Статистика', 'action': show_stat},
    # 'help': {'title': 'Справка', 'action': show_help},
}



# async def show_help(message: Message, state: FSMContext):
#     await message.answer(MESSAGES['help'], reply_markup=ReplyKeyboardRemove())