data_saved_message = 'Данные успешно сохранены: \n{}'
bad_answer_message = 'Ответ не соответствует формату.\nПопробуйте ещё раз.'


MESSAGES = {
    # 'start': start_message,
    # 'help': '\n'.join([f'/{key} -- {value.get("title","")}'
    #                    for key, value in MAIN_MENU.items()]),
    # 'invalid_key': invalid_key_message,
    'data_saved': data_saved_message,
    'bad_answer': bad_answer_message,
    'response': 'Откликнуться'
}


create_vacanse_dialog_config = {
    'questions': {
        'photo': {
            'text': 'Фото',
            'type': 'photo',
        },
        'discription': {
            'text': 'Опишите вакансию',
            'loop_stop_word': 'Закончить с описанием',
        },
        'questions': {
            'text': 'Задайте вопрос соискателю',
            'loop_stop_word': 'Достаточно вопросов'
        }
    },
    'order': ['discription', 'questions', 'photo', ]
}

