from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON, TEXT
from sqlalchemy.dialects.postgresql.base import BYTEA

from lib_telechatbot.models.abstract_BaseModelWithTelegam import BaseModelWithTelegram
from models.UserList import UserList


class Vacanse(BaseModelWithTelegram):
    __tablename__ = 'vacanse'
    image = Column(BYTEA)
    discriptions = Column(ARRAY(TEXT, dimensions=1))    
    questions = Column(ARRAY(TEXT, dimensions=1))

    user_id = Column(
        UUID, ForeignKey(f'{UserList.__tablename__}.id', ondelete='CASCADE'),
        nullable=False, index=True)



