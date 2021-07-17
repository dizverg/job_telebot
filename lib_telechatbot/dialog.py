import datetime
from messages import MESSAGES
from aiogram import types, Dispatcher
from models import Category, CategoryItem


class Dialog:
    order = []
    questions = dict()

    def __init__(self, config):
        self.questions = config.get('questions')
        self.order = config.get('order')
        self.dialog_state = config.get('state')

    async def check_answer(self, data, message):
        answer = message.text
        if not self.type_check(answer, data):
            await message.answer(MESSAGES['bad_answer'])
            return False
        return True

    @staticmethod
    def type_check(answer, data):
        try:
            return {'int': answer.isnumeric,
                    'select_one': lambda: answer in data.get('variants'),
                    'date': lambda: datetime.datetime.strptime(answer,
                                                               '%d.%m.%Y'),
                    'select_one_or_type': lambda: True,
                    '*': lambda: True
                    }.get(data.get('type', '*'), False)()
        except:
            return False

    def get_first(self):
        try:
            return self.order[0]
        except:
            return

    def get_parameter_by_name(self, current: str = None) -> dict:
        return self.questions.get(current, dict())

    def get_next(self, current: str = None) -> str:
        try:
            return self.order[self.order.index(current) + 1]
        except:
            return ""

    async def ask(self, message: types.Message,
                  parameter_name: str = ""):
        parameter = self.get_parameter_by_name(parameter_name)
        if not parameter:
            return
        category_variants = [
            item.name for item in CategoryItem.filter_by(
                category_id=Category.get_id_by_name(parameter.get('category'))
            ).all()]

        parameter['variants'] = category_variants or parameter.get('variants')

        if parameter['variants']:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*parameter['variants'])
        else:
            keyboard = types.ReplyKeyboardRemove()

        await self.dialog_state.set()
        await message.answer(parameter.get('text'), reply_markup=keyboard)
        await Dispatcher.get_current().current_state().update_data(
            {'current_field': parameter_name, 'dialog': self})

    async def get_answer(self, message, state, on_finish=None):
        answer = message.text
        field_name = (await state.get_data()).get('current_field')
        check_result = await self.check_answer(
            self.get_parameter_by_name(field_name), message)
        if not check_result:
            await self.ask(message=message, parameter_name=field_name)
            return
        await state.update_data({field_name: answer})
        next_field = self.get_next(field_name)
        if next_field:
            # print(str(await state.get_data()))
            await self.ask(message=message, parameter_name=next_field)
        else:
            await state.update_data({'current_field': None})
            await on_finish(message=message, state=state)
            await state.finish()

    # callback_data = cb.new(parameter=parameter_name, state=state)

    # dialog_states = DialogStates()
    # for question in dialog.get('questions', list()):
    # dialog_states.__setattr__(name=question, value=State())
    # ...

    # cb = CallbackData('action', "parameter", "state")
