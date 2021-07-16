from menu import Menu

from aiogram import types
from aiogram.dispatcher import  FSMContext, filters
from aiogram.types import ContentTypes, Message
from aiogram.utils import executor


from dialog import Dialog
from messages import DIALOGS, MENU, MESSAGES
from models import UserList, Board, Tutorial
from states import DialogState

from telechatbot.bot_dispatcher import dp


async def auth(message: Message, state: FSMContext):
    user = (await state.get_data()).get(
        'user', await UserList.get_user(message.from_user.id))
    if user:
        await state.update_data({'user': user})
        return user
    else:
        return


async def finish_dialog(message: Message, state: FSMContext, *args, **kwargs):
    await message.answer(str(await state.get_data()),
                         reply_markup=(types.ReplyKeyboardRemove()))


async def init_dialog(message: Message, state: FSMContext, command: str):
    await auth(message, state)
    dialog = Dialog(config=DIALOGS[command])
    await state.update_data({'dialog': dialog})
    await dialog.ask(message=message, parameter_name=dialog.get_first())


async def get_answer(message: Message, state: FSMContext, on_finish=None):
    try:
        await ((await state.get_data()
                ).get('dialog')).get_answer(message, state, on_finish)
    except:
        ...


@dp.message_handler(commands="start", state="*")
async def start(message: Message):
    await message.reply(
        MESSAGES['start'], reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands="help", state="*")
async def help(message: Message):
    await message.reply(
        MESSAGES['help'], reply_markup=types.ReplyKeyboardRemove())


# profile
async def show_profile(message: Message, user: UserList):
    await message.reply(user)


# async def create_new_profile(
#         message: Message, state: FSMContext, command: str):
#     # await state.update_data({'user': None})
#     await init_dialog(message, state, command)


@dp.message_handler(commands=['new_profile'], state="*")
async def new_profile(message: Message, state: FSMContext):
    user = (await state.get_data()).get(
        'user', await UserList.get_user(message.from_user.id))
    if user:
        await state.update_data({'user': user})
    await init_dialog(message, state, 'profile')


@dp.message_handler(commands=["profile"], state="*")
async def profile(message: Message, state: FSMContext):
    user = (await state.get_data()).get(
        'user', await UserList.get_user(message.from_user.id))
    if user:
        await DialogState.profile_wait_for_answer.set()
        await state.update_data({'user': user})
        await show_profile(message, user)
        # await init_dialog(message, state, command)
    else:
        await init_dialog(message, state, 'profile')


async def profile_finish_dialog(message: Message, state: FSMContext):
    data = await state.get_data()
    from_user = message.from_user
    user = data.pop('user')
    data.pop('dialog')
    data.pop('current_field')
    new_data = {'json': data,
                'telegram_id': from_user.id,
                'username': from_user.username,
                'is_bot': from_user.is_bot,
                'language_code': from_user.language_code,
                'first_name': from_user.first_name}
    if user:
        user.update(new_data)
    else:
        UserList(**new_data).add()
    # await message.reply(state)
    await message.answer(str(MESSAGES.get('data_saved', '{}')).format(data),
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=DialogState.profile_wait_for_answer)
async def profile_get_answer(message: Message, state: FSMContext):
    await get_answer(message, state, profile_finish_dialog)


# manuals board
@dp.message_handler(commands=["manuals", "board"], state="*")
async def manuals_board_sectors(message: Message, state: FSMContext,
                                command: filters.Command.CommandObj):
    await init_dialog(message, state, command.command)


async def board_finish_dialog(message: Message, state: FSMContext):
    data = await state.get_data()
    from_user = message.from_user
    user = data.pop('user')
    data.pop('dialog')
    data.pop('current_field')
    new_data = {'json': data,
                'user_id': user.id,
                'telegram_id': from_user.id}

    Board(**new_data).add()
    # await message.reply(state)
    await message.answer(str(MESSAGES.get('data_saved', '{}')).format(data),
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=DialogState.board_wait_for_answer)
async def board_get_answer(message: Message, state: FSMContext):
    await ((await state.get_data()).get('dialog')
           ).get_answer(message, state, board_finish_dialog)


async def manuals_finish_dialog(message: Message, state: FSMContext):
    data = await state.get_data()
    from_user = message.from_user
    user = data.pop('user')
    data.pop('dialog')
    data.pop('current_field')
    new_data = {'json': data,
                'user_id': user.id,
                'telegram_id': from_user.id}

    Tutorial(**new_data).add()
    # await message.reply(state)
    await message.answer(str(MESSAGES.get('data_saved', '{}')).format(data),
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=DialogState.manuals_wait_for_answer)
async def manuals_get_answer(message: Message, state: FSMContext):
    await ((await state.get_data()).get('dialog')
           ).get_answer(message, state, manuals_finish_dialog)


@dp.message_handler(state="*", content_types=ContentTypes.TEXT)
async def echo(message: Message):
    await message.reply(message.as_json(),
                        reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    # init_db()
    # menu = Menu(MENU['Главное меню'])
    # print(menu)
    executor.start_polling(dp)
