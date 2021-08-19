from aiogram.types.inline_keyboard import InlineKeyboardMarkup
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from models import Applicant, Vacancy
from aiogram.types.callback_query import CallbackQuery
from lib.bot_dispatcher import applicant_bot
from cfg.messages import MESSAGES


async def applicant_respond_callback(callback_query: CallbackQuery):
    await callback_query.message.delete_reply_markup()
    vacancy_id = callback_query.data.split()[1]

    # await applicant_bot.answer_callback_query(
    #     callback_query.id,
    #     text=MESSAGES['response_registered'],
    #     show_alert=False)



    # TODO check not response

    from dialogs.respond_dialog import RespondDialog
    await RespondDialog.begin(
        chat_id=callback_query.from_user.id,
        config=(Vacancy.find_by_id(vacancy_id).questions or []) + [{
            'name': 'video',
            'text': MESSAGES['upload_video'],
            'type': 'video'
        }],
        vacancy_id=vacancy_id
    )

    await callback_query.bot.answer_callback_query(callback_query.id)


async def hr_respond_callback(callback_query: CallbackQuery):
    _, applicant_id = callback_query.data.split()
    Applicant().update(applicant_id, {'accepted': False})

    await callback_query.message.delete_reply_markup()
    await callback_query.answer('Отклонено')
    # await bot.send_message(callback_query.from_user.id, callback_query.data)


async def show_user_link_respond_callback(callback_query: CallbackQuery):
    _, user_id, applicant_id = callback_query.data.split()
    md_user_caption = f'[Кандидат ]'
    message = callback_query.message
    if not message.text or not message.md_text.startswith(md_user_caption):
        Applicant().update(applicant_id, {'accepted': True})
        await message.edit_text(
            md_user_caption +
            f'(tg://user?id={user_id})' +
            f'\n\n{message.text or ""}',
            parse_mode='Markdown',
            # reply_markup=ReplyKeyboardRemove()
            # InlineKeyboardMarkup().add(
            # message.reply_markup.inline_keyboard[0][1])
        )
