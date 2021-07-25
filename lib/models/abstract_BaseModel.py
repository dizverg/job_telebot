import uuid

from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from lib.db import Base, Session


class BaseModel(Base):
    __abstract__ = True
    # id = Column(Integer, primary_key=True,  autoincrement=True)
    id = Column(UUID, default=lambda: str(uuid.uuid4()), primary_key=True)

    # created_at = Column(TIMESTAMP, nullable=True,
    #                     default=lambda: datetime.now())
    # updated_at = Column(TIMESTAMP, nullable=True,
    #                     default=lambda: datetime.now())

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id!r})>"

    def add(self):
        with Session() as session:
            session.add(self)
            session.commit()
            return self.id

    def update(self, id, data):
        with Session() as session:
            self.filter_by(id=id).update(data)
            session.commit()
            return self.id

    def delete(self):
        with Session() as session:
            session.delete(self)
            session.commit()

    @classmethod
    def query(cls):
        return Session().query(cls)

    @classmethod
    def filter_by(cls, **kwargs):
        return cls.query().filter_by(**kwargs)

    @classmethod
    def filter(cls, expression: BinaryExpression):
        return cls.query().filter(expression)

    @classmethod
    def find_by_id(cls, id):
        return cls.filter_by(id=id).one()

    @classmethod
    def delete_by_id(cls, id):
        cls.filter_by(id=id).one().delete()

    @classmethod
    def all(cls):
        return cls.query().all()
