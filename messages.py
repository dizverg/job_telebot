from aiogram.dispatcher.filters.state import State
from main_menu_actions import (list_published, list_waiting_applicants,
                               publish, show_help, show_stat)


# start_message = 'Let`s go!\n' + help_message
# invalid_key_message = 'Ключ "{key}" не подходит.\n' + help_message
state_change_success_message = 'Текущее состояние успешно изменено'
state_reset_message = 'Состояние успешно сброшено'
current_state_message = 'Текущее состояние - "{current_state}",' \
                        ' что удовлетворяет условию "один из {states}"'
data_saved_message = 'Данные успешно сохранены: \n{}'
bad_answer_message = 'Ответ не соответствует формату.\nПопробуйте ещё раз.'


MAIN_MENU = {
    'published': {'title': 'Опубликованные вакансии', 'action': list_published},
    'publish': {'title': 'Опубликовать вакансию', 'action': publish},
    'applicants': {
        'title': 'Соискатили в ожидании ответа',
        'action': list_waiting_applicants
    },
    'stat': {'title': 'Статистика', 'action': show_stat},
    'help': {'title': 'Справка', 'action': show_help},
}

MESSAGES = {
    # 'start': start_message,
    'help': '\n'.join([f'/{key} -- {value.get("title","")}'
                       for key, value in MAIN_MENU.items()]),
    # 'invalid_key': invalid_key_message,
    'state_change': state_change_success_message,
    'state_reset': state_reset_message,
    'current_state': current_state_message,
    'data_saved': data_saved_message,
    'bad_answer': bad_answer_message,
}



