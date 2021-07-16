from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from models.Category import Category
from models.abstract_BaseModel import BaseModel


class CategoryItem(BaseModel):
    __tablename__ = 'category_item'
    category_id = Column(
        UUID, ForeignKey(f'{Category.__tablename__}.id',
                         ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255))
    parent_id = Column(UUID, nullable=True, index=True)

    def __repr__(self):
        return (f"<{self.__class__.__name__}("
                f"id={self.id!r}, name={self.name!r})>")
