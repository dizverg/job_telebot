import datetime
from messages import MENU, MESSAGES
from aiogram import types, Dispatcher
from models import Category, CategoryItem


class Menu:
    tree = dict()

    def __init__(self, config):
        self.tree = config

    def get_items(self):
        return [*self.tree]

    # async def check_answer(self, data, message):
    #     answer = message.text
    #     if not self.type_check(answer, data):
    #         await message.answer(MESSAGES['bad_answer'])
    #         return False
    #     return True

    # @staticmethod
    # def type_check(answer, data):
    #     try:
    #         return answer in data.get('variants')
    #     except:
    #         return False

    # def get_first(self):
    #     try:
    #         return self.order[0]
    #     except:
    #         return

    # def get_parameter_by_name(self, current: str = None) -> dict:
    #     return self.questions.get(current, dict())

    async def ask(self, message: types.Message, ask_text:str):

        variants = self.tree.get_items()

        if variants:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*variants)
        else:
            keyboard = types.ReplyKeyboardRemove()

        await self.menu_state.set()
        await message.answer(ask_text, reply_markup=keyboard)
        # await Dispatcher.get_current().current_state().update_data('menu': self})

    async def get_answer(self, message, state, on_finish=None):
        answer = message.text
        # check_result = await self.check_answer(
        #     self.get_parameter_by_name(field_name), message)
        # if not check_result:
        #     await self.ask(message=message, ask_text=ask_text)
        #     return
#TODO 

if __name__ == '__main__':
    # init_db()
    root = MENU['Главное меню']
    menu = Menu(root)
    item = menu.get_items()[0]
    print(f'item: {item}')
    submenu = root[item]
    print(f'submenu: {submenu}')
    nemu2 = Menu(submenu)
    items = nemu2.get_items()
    print(items[0])

