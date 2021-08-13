from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON, TEXT
from sqlalchemy.dialects.postgresql.base import BYTEA

from lib.abstract_BaseModelWithTelegam import BaseModelWithTelegram
from models.UserList import UserList


class Vacancy(BaseModelWithTelegram):
    __tablename__ = 'vacancy'
    photo = Column(TEXT)
    descriptions = Column(ARRAY(TEXT, dimensions=1))
    questions = Column(ARRAY(TEXT, dimensions=1))

    user_id = Column(
        UUID, ForeignKey(f'{UserList.__tablename__}.id', ondelete='CASCADE'),
        nullable=False, index=True)

    def __repr__(self):
        description = f"Описание ваансии:\n{self.get_description()}"
        questions = f"Вопросы:\n" + '\n'.join(self.questions) if self.questions else ""
        return '\n\n'.join((description, questions))

    def get_description(self):
        return '\n'.join(self.descriptions) if self.descriptions else " "
