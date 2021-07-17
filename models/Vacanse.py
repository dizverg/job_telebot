from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from lib_telechatbot.models.abstract_BaseModelWithTelegam import BaseModelWithTelegram
from models.UserList import UserList


class Vacanse(BaseModelWithTelegram):
    __tablename__ = 'vacanse'
    user_id = Column(
        UUID, ForeignKey(f'{UserList.__tablename__}.id', ondelete='CASCADE'),
        nullable=False, index=True)



