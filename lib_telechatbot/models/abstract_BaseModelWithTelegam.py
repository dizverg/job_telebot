from sqlalchemy import Column, Integer, TIMESTAMP
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from  lib_telechatbot.models.abstract_BaseModel import BaseModel


class BaseModelWithTelegram(BaseModel):
    __abstract__ = True
    json = Column(JSON)
    tags = Column(ARRAY(UUID))
    telegram_id = Column(Integer)
    telegram_date = Column(TIMESTAMP)

    def __repr__(self):
        return f"<{self.__class__.__name__}(" \
               f"id={self.id!r}, json={self.json!r}, tags={self.tags!r})>"
