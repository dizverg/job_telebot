from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from models.abstract_BaseModelWithTelegam import BaseModelWithTelegram
from models.UserList import UserList


class Tutorial(BaseModelWithTelegram):
    __tablename__ = 'tutorial'
    user_id = Column(
        UUID, ForeignKey(f'{UserList.__tablename__}.id', ondelete='CASCADE'),
        nullable=False, index=True)

