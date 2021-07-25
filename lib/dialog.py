from datetime import datetime
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from models import Category, CategoryItem
from lib.bot_dispatcher import applicant_bot, bot_dispatcher


class Dialog:

    def __init__(self, config, bot=None):

        self.bot = bot or applicant_bot
        self.config = config

        if type(config) == dict:
            self.questions = config.get('questions')
            self.order = config.get('order')
        elif type(config) == list:
            self.questions = {v: {'text': v, 'type': '*'} for v in config}
            self.order = config
        else:
            raise

    async def check_answer(self, data, message):
        if not self.type_check(message, data):
            from messages import MESSAGES

            await message.answer(MESSAGES['bad_answer'])
            return False
        return True

    @staticmethod
    def type_check(message: Message, data):
        # try:
        text = message.text
        data_types = data.get('type', '*')
        data_types = data_types if type(data_types) == list else [data_types]
        for data_type in data_types:
            if {'int': text.isnumeric if text else False,
                    'select_one': lambda: text in data.get('variants'),
                    'date': lambda: datetime.strptime(text, '%d.%m.%Y'),
                        'select_one_or_type': lambda: True,
                        '*': lambda: True,
                            'photo': lambda: bool(message.photo)
                    }.get(data_type, lambda: False)():
                return True
        # finally:
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

    async def ask(self, from_user_id: int, parameter_name):

        parameter = self.get_parameter_by_name(parameter_name)
        if not parameter:
            return
        category_variants = [
            item.name for item in CategoryItem.filter_by(
                category_id=Category.get_id_by_name(parameter.get('category'))
            ).all()]

        keys = category_variants or parameter.get('variants') or []
        loop_stop_word = parameter.get('loop_stop_word')
        if loop_stop_word:
            keys.append(loop_stop_word)

        if keys:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*keys)
        else:
            keyboard = ReplyKeyboardRemove()

        await self.bot.send_message(from_user_id,
                                    parameter.get('text'), reply_markup=keyboard)

        state = bot_dispatcher.current_state(chat=from_user_id)
        await state.update_data(
            {'current_field': parameter_name, 
             'loop_stop_word': loop_stop_word})


    async def get_answer(self, message: Message, state: FSMContext, on_finish=None):
        text = message.text

        data = await  state.get_data()

        field_name = data.get('current_field')
        field_value = data.get(field_name)
        check_result = await self.check_answer(
            self.get_parameter_by_name(field_name), message)

        if not check_result:
            await self.ask(
                from_user_id=message.from_user.id,
                parameter_name=field_name)
            return

        field_value = (field_value if type(field_value) == list
                       else [field_value] if field_value else [])

        loop_stop_word = data.get('loop_stop_word')
        # if not loop_stop_word or loop_stop_word == answer:

        if message.photo:
            await state.update_data({field_name + '_photo': message.photo[-1]})

        if message.video:
            await state.update_data({field_name + '_video': message.video[-1]})

        if loop_stop_word != text:
            await state.update_data({field_name: field_value + [text]})

        next_field = (field_name if loop_stop_word and loop_stop_word != text
                      else self.get_next(field_name))

        if next_field:
            # print(str(await state.get_data()))
            await self.ask(
                from_user_id=message.from_user.id,
                parameter_name=next_field)
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
