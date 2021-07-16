from db import Base, engine
from models import Category, CategoryItem

CATEGORIES = {
    'country': [
        {'name': 'Россия',
         'city': ['Москва', 'Санкт-Питербург', 'Уфа', 'Выборг', 'Омск'],
         'city2': ['Москва2']
         },
        {'name': 'Белоруссия', 'city': ['Минск']},
        'Казахстан'
    ],
    'fuel_type': ['бензин', 'дизель', 'метан', 'бутан', 'электро'],
    'color': ['красный', 'синий', 'зелёный', 'белый', 'чёрный'],
    'auto_model': ['красненькая', 'зелёненькая', 'беленькая'],
    'yes_no': ['да', 'нет'],
    'yes_no_cancel': ['да', 'нет', 'отмена'],
    'navigation': ['назад', 'перейти', 'вперёд'],
    'number': [1, 2, 3, 4, 5],
}


def fill_categories(categories: dict, parent_id=None):
    for category_name, category_list in categories.items():
        if type(category_list) == str:
            continue

        category_id = Category.get_id_by_name(
            category_name) or Category(name=category_name).add()

        for category_item in category_list:
            item_type = type(category_item)
            category_item_name = (
                category_item if item_type == str
                else category_item.get('name') if item_type == dict
                else str(category_item))
            new_item_id = CategoryItem(category_id=category_id,
                                       parent_id=parent_id,
                                       name=category_item_name).add()

            if item_type == dict:
                fill_categories(categories=category_item,
                                parent_id=new_item_id)


def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    fill_categories(CATEGORIES)


if __name__ == '__main__':
    init_db()
    print(Category.all())
    print(CategoryItem.all())
