from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup

from cfg.messages import MESSAGES
from lib.base_dialog import AuthMixin
from lib.bot_dispatcher import publisher_bot
from models import Applicant
from models import Vacancy
from dialogs.publisher_dialog import PublisherDialog
from dialogs.respond_dialog import RespondDialog


async def publish(message: Message, state: FSMContext):
    await PublisherDialog.begin(message.chat.id)


async def list_published(message: Message, state: FSMContext):
    for vacancy in Vacancy.all():
        await message.answer_photo(photo=vacancy.photo,
                                   caption=vacancy,
                                   reply_markup=ReplyKeyboardRemove())


async def list_vacancies(message: Message, state: FSMContext):
    applicants = Applicant.filter_by(
        user_id=AuthMixin.get_user_id(message.from_user)).all()
    used_vacancies = [applicant.vacancy_id for applicant in applicants]
    for vacancy in Vacancy.filter(Vacancy.id not in used_vacancies).all():
        if vacancy.id in used_vacancies:
            continue
        await message.bot.send_photo(
            chat_id=message.chat.id,
            photo=await publisher_bot.download_file_by_id(vacancy.photo),
            caption=vacancy.get_description() or '-',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(MESSAGES['response'],
                                     callback_data=f'respond {vacancy.id}')))

        # await message.answer_photo(
        #     photo=await publisher_bot.download_file_by_id(vacancy.photo),
        #     caption=vacancy,
        #     reply_markup=ReplyKeyboardRemove())


async def list_waiting_applicants(message: Message, state: FSMContext):
    for applicant in Applicant.filter_by(accepted=None).all():
        await message.answer(applicant, reply_markup=ReplyKeyboardRemove())


async def show_stat(message: Message, state: FSMContext):
    markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('?????????????????? ???????? ?????????????? ??????', request_contact=True))

    vacancy_count = Vacancy.query().count()
    waiting_count = Applicant.filter_by(accepted=None).count()
    accepted_count = Applicant.filter_by(accepted=True).count()
    rejected_count = Applicant.filter_by(accepted=False).count()
    await message.answer(
        f"???????????????????????? ????????????????: {vacancy_count}\n"
        f"????????????????: {accepted_count}\n"
        f"??????????????????: {rejected_count}\n"
        f"?? ????????????????: {waiting_count}\n",
        # reply_markup=markup_request
        reply_markup=ReplyKeyboardRemove()
    )


PUBLISHER_MENU = {
    'published': {'title': '?????????????????????? ?????????????????????????? ????????????????',
                  'action': list_published},
    'publish': {'title': '???????????????????????? ????????????????', 'action': publish},
    'applicants': {'title': '???????????????????? ?? ???????????????? ????????????',
                   'action': list_waiting_applicants},
    'stat': {'title': '????????????????????', 'action': show_stat},

}


async def applicant_start(message: Message, state: FSMContext):
    data = message.text.split()
    vacancy_id = data[1] if len(data) > 1 else None
    if vacancy_id:
        vacancy = Vacancy.find_by_id(vacancy_id)

        # await message.answer(vacancy_id,
        #                      reply_markup=ReplyKeyboardRemove())
        await message.bot.send_photo(
            chat_id=message.chat.id,
            photo=await publisher_bot.download_file_by_id(vacancy.photo),
            caption=vacancy.get_description() or '-',
            reply_markup=ReplyKeyboardRemove()
        )

        await RespondDialog.begin(
            chat_id=message.from_user.id,
            config=(vacancy.questions or []) + [
                {
                    'name': 'video_note',
                    'text': MESSAGES['upload_video'],
                    'type': 'video_note'
                }
            ],
            vacancy_id=vacancy_id
        )
    else:
        await message.answer(MESSAGES['applicant_start'],
                             reply_markup=ReplyKeyboardRemove())


APPLICANT_MENU = {
    'start': {'title': '????????????', 'action': applicant_start},
    # 'help': {'title': '??????????????', 'action': applicant_start},
    'vacancy': {'title': '?????????????????????? ????????????????',
                'action': list_vacancies},
    # 'help': {'title': '??????????????', 'action': show_help},
    'stat': {'title': '????????????????????', 'action': show_stat},

}
