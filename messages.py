from actions import (active_deals_list, add_car, buy,
                     edit_settings, my_ad_list, reset_settings, sell)
from states import DialogState

help_message = ('Для того, чтобы посмотреть справочную информацию, '
                'отправь команду "/help"\n'
                '"/profile" -- просмотра или изменение профиля пользователя\n'
                '"/board" -- управление объявлениями\n'
                '"/manuals" -- техничка\n'
                )

start_message = 'Let`s go!\n' + help_message
invalid_key_message = 'Ключ "{key}" не подходит.\n' + help_message
state_change_success_message = 'Текущее состояние успешно изменено'
state_reset_message = 'Состояние успешно сброшено'
current_state_message = 'Текущее состояние - "{current_state}",' \
                        ' что удовлетворяет условию "один из {states}"'
data_saved_message = 'Данные успешно сохранены: \n{}'
bad_answer_message = 'Ответ не соответствует формату.\nПопробуйте ещё раз.'

MESSAGES = {
    'start': start_message,
    'help': help_message,
    'invalid_key': invalid_key_message,
    'state_change': state_change_success_message,
    'state_reset': state_reset_message,
    'current_state': current_state_message,
    'data_saved': data_saved_message,
    'bad_answer': bad_answer_message,
}

profile_dialog_config = {
    'questions': {
        'county': {
            'text': 'Выберите страну',
            'type': 'select_one',
            'category': 'country',
        },
        'city': {
            'text': 'Укажите ваш город',
            'type': 'select_one_or_type',
            'category': 'city',
        },
        'birthday': {
            'text': 'Укажите дату вашего рождения в формате ДД.ММ.ГГГГ',
            'type': 'date'
        },
        'yes_no_cancel': {
            'text': 'Да, нет или отмена?',
            'type': 'select_one',
            'category': 'yes_no_cancel',
        },
        'pet_name': {
            'text': 'Как зовут вашего питомца?',
            'type': '*',
        },
        'yes_no': {
            'text': 'Да, нет?',
            'type': 'select_one',
            'variants': ['yes', 'no_cancel'],
        }
    },
    'order': ['pet_name', 'yes_no_cancel', 'county', 'yes_no',
              # 'birthday'
              ],
    # 'order': ['yes_no_cancel', 'city'],
    'state': DialogState.profile_wait_for_answer
}

board_dialog_config = {
    'questions': {
        'model': {
            'text': 'Какая у вас модель автомобиля?',
            'type': 'select_one_or_type',
            'category': 'auto_model',
        },
        'year': {
            'text': 'Какого года автомобиль?',
            'type': 'int',
        },
        'fuel_type': {
            'text': 'На каком топливе работает двигатель?',
            'type': 'select_one',
            'category': 'fuel_type',
        },
        'yes_no': {
            'text': 'Да или нет?',
            'type': 'select_one',
            'category': 'yes_no',
        }
    },
    'order': ['yes_no', 'model', 'year', 'fuel_type'],
    'state': DialogState.board_wait_for_answer
}

manuals_dialog_config = {
    'questions': {
        'model': {
            'text': 'О каком модели пост?',
            'type': 'select_one_or_type',
            'category': 'auto_model',
        },
        'year': {
            'text': 'Какого года автомобиль?',
            'type': 'int',
        },
        'fuel_type': {
            'text': 'На каком топливе работает двигатель?',
            'type': 'select_one',
            'category': 'fuel_type',
        }
    },
    'order': ['model', 'year', 'fuel_type'],
    'state': DialogState.manuals_wait_for_answer
}

DIALOGS = {
    'profile': profile_dialog_config,
    'board': board_dialog_config,
    'manuals': manuals_dialog_config
}


MENU = {
    'Главное меню': {
        'Маркет': {
            'Активные сделки': active_deals_list,
            'Мои объявления': my_ad_list,
            'Купить': buy,
            'Продать': sell,
            'Главное меню': 'Главное меню'
        },
        'Настройки': {
            'Сбрость': reset_settings,
            'Редактировать': edit_settings,
            'Главное меню': 'Главное меню'
        },
        'Мои машины': {
            'Показать': 'Мои машины',
            'Добавить': add_car,
            'Главное меню': 'Главное меню'
        }
    }

}
