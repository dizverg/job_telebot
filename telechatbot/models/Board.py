from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from models.abstract_BaseModelWithTelegam import BaseModelWithTelegram
from models.UserList import UserList


class Board(BaseModelWithTelegram):
    __tablename__ = 'board'
    user_id = Column(
        UUID, ForeignKey(f'{UserList.__tablename__}.id', ondelete='CASCADE'),
        nullable=False, index=True)



