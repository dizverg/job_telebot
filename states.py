from aiogram.dispatcher.filters.state import StatesGroup, State


class DialogState(StatesGroup):
    default = State()
    # profile_mode = State()
    profile_wait_for_answer = State()
    manuals_wait_for_answer = State()
    board_wait_for_answer = State()
