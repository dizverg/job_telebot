from models import Vacanse
from aiogram.types.callback_query import CallbackQuery
from dialogs.respond_dialog import RespondDialog, applicant_respond_callback
from lib.bot_dispatcher import applicant_bot

async def applicant_respond_callback(callback_query: CallbackQuery):
    vacanse_id = callback_query.data.split(' ')[1]

    await applicant_bot.answer_callback_query(
        callback_query.id, text=callback_query.data, show_alert=False)

    response_dialog = RespondDialog(
        config=Vacanse.find_by_id(vacanse_id).questions,
    )

    await response_dialog.begin(from_user=callback_query.from_user)

    # await bot.send_message(callback_query.from_user.id, callback_query.data)
    
CALLBACKS = {
    'applicant_ui': applicant_respond_callback,
    # 'hr_ui':hr_callback
}
