from sqlalchemy import Column, String, Boolean

from lib.models.abstract_BaseModelWithTelegam import BaseModelWithTelegram


class UserList(BaseModelWithTelegram):
    __tablename__ = 'user_list'
    username = Column(String(255))
    first_name = Column(String(255))
    language_code = Column(String(255))
    is_bot = Column(Boolean)
    message_id = Column(String(255))

    @classmethod
    async def get_user(cls, user_telegram_id):
        user = cls.filter_by(telegram_id=user_telegram_id).limit(1).all()
        if user:
            return user[0]

    def __repr__(self):
        return (f"Приветствую тебя,"
                f" {self.first_name or ''} {self.username or ''}!\n\n"
                f"Вот, что я знаю о тебе:\n{self.json!r}"
                f"\n\n/new_profile -- заполнить анкету занова")
        # return (f"<{self.__class__.__name__}("
        #         f"id={self.id!r}, "
        #         f"username={self.username!r}, "
        #         f"first_name={self.id!r}, "
        #         f"json={self.json!r}, "
        #         f"tags={self.tags!r})>")

