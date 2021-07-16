from sqlalchemy import Column, String, Boolean
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from telechatbot.models.abstract_BaseModelWithTelegam import BaseModelWithTelegram

from models.UserList import UserList

class Applicant(BaseModelWithTelegram):
    __tablename__ = 'applicant'
    user_id = Column(
        UUID, ForeignKey(f'{UserList.__tablename__}.id', ondelete='CASCADE'),
        nullable=False, index=True)