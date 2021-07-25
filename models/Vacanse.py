from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON, TEXT
from sqlalchemy.dialects.postgresql.base import BYTEA

from lib.models.abstract_BaseModelWithTelegam import BaseModelWithTelegram
from models.UserList import UserList


class Vacanse(BaseModelWithTelegram):
    __tablename__ = 'vacanse'
    photo = Column(TEXT)
    discriptions = Column(ARRAY(TEXT, dimensions=1))
    questions = Column(ARRAY(TEXT, dimensions=1))

    user_id = Column(
        UUID, ForeignKey(f'{UserList.__tablename__}.id', ondelete='CASCADE'),
        nullable=False, index=True)

    def __repr__(self):
        discription = f"Описание ваансии:\n" + self.get_discription()
        questions = f"Вопросы:\n" + '\n'.join(self.questions if self.questions else "")
        return '\n\n'.join((discription, questions))

    def get_discription(self):
        return '\n'.join( self.discriptions if self.discriptions else "")
