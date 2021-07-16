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


create_vacanse_dialog_config = {
    'questions': {
        'photo': {
            'text': 'Фото',
            'type': 'image',
        },
        'discription': {
            'text': 'Опишите вакансию',
            'variants': ['Закончить с описанием'],
        },
        'questions': {
            'text': 'Задайте вопрос соискателю',
            'variants': ['Достаточно вопросов'],
            'array': True,
        }
    },
    'order': ['yes_no', 'model', 'year', 'fuel_type'],
    'state': DialogState.board_wait_for_answer
}

DIALOGS = {
    'create_vacanse': create_vacanse_dialog_config,
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


MENU2 = {
        'Публикация': {
            'Опубликованные': list_published,
            'Неопубликованные': list_not_published,
            'Опубликовать': publish,
        },
        'HR': {
            'Соискатели в ожидании': list_waiting_applicants,
        }
}
