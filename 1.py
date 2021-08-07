from os import stat
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
from aiogram.dispatcher.filters.state import State, StatesGroup

class PublishStates(StatesGroup):
    discription = State()
    questions = State()
    photo = State()

PublishStates.a=State()

for x in PublishStates.states:
    print(x)