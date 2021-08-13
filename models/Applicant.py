from models.Vacancy import Vacancy
from aiogram.types import video
from sqlalchemy import Column, String, Boolean
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TEXT
from lib.models.abstract_BaseModelWithTelegam import BaseModelWithTelegram

from models.UserList import UserList


class Applicant(BaseModelWithTelegram):
    __tablename__ = 'applicant'  
    user_id = Column(
        UUID, ForeignKey(f'{UserList.__tablename__}.id', ondelete='CASCADE'),
        nullable=False, index=True)

    # vacancy_id = Column(
    #     UUID, ForeignKey(f'{Vacancy.__tablename__}.id', ondelete='CASCADE'),
    #     nullable=False, index=True)

    video = Column(TEXT)

    accepted = Column(Boolean, nullable=True, index=True, default=None)