from sqlalchemy import Column, String

from lib_telechatbot.db import Session
from lib_telechatbot.models.abstract_BaseModel import BaseModel


class Category(BaseModel):
    __tablename__ = 'category'
    name = Column(String(255))
    title = Column(String(255))

    @classmethod
    def get_id_by_name(cls, name):
        try:
            return Session().query(cls).filter(
                cls.name == name).limit(1).one().id
        except:
            return None

    def __repr__(self):
        return f"<{self.__class__.__name__}(" \
               f"id={self.id!r}, name={self.name!r}, title={self.title!r})>"
