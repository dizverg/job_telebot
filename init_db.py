from models.Applicant import Applicant
from models.Vacanse import Vacanse
from models.UserList import UserList
from telechatbot.db import Base, engine
from models import Category, CategoryItem


def init_db():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # fill_categories(CATEGORIES)
    user_id = UserList().add()
    Vacanse(user_id=user_id).add()
    Vacanse(user_id=user_id).add()
    Applicant(user_id=user_id).add()
    Applicant(user_id=user_id).add()


if __name__ == '__main__':
    init_db()
    # print(Category.all())
    # print(CategoryItem.all())
