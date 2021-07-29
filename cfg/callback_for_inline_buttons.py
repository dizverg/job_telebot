from models import Vacanse
from aiogram.types.callback_query import CallbackQuery
from dialogs.respond_dialog import RespondDialog
from lib.bot_dispatcher import applicant_bot


async def applicant_respond_callback(callback_query: CallbackQuery):
    vacanse_id = callback_query.data.split(' ')[1]

    await applicant_bot.answer_callback_query(
        callback_query.id,
        text=callback_query.data,
        show_alert=False)
    vacanse = Vacanse.find_by_id(vacanse_id)

    await RespondDialog.begin(
        chat_id=callback_query.from_user.id,
        config=vacanse.questions,
        vacanse_id=vacanse_id
    )

    # await bot.send_message(callback_query.from_user.id, callback_query.data)
