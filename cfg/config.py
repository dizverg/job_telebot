import logging
import sys

from cfg.private_token import tokens, DB_Private

MODE = sys.argv[1] if len(sys.argv) > 1 else None
TOKEN = tokens.get(MODE or list(tokens)[0])

LOG = {'format': "%(asctime)s - [%(levelname)s] - %(name)s - "
                 "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
       'level': logging.INFO}

CHANNEL_ID = -1001568792005
HR_ID = -1001347207892


class DB_PG(DB_Private):
    filename = 'job_telebot.db'
    db_name = 'job_telebot'
    dialect_plus_driver = 'postgresql+psycopg2'

    @classmethod
    def get_db_url(cls):
        return f"{cls.dialect_plus_driver}://{cls.user}" \
               f"{f':{cls.password}' if cls.password else ''}@" \
               f"{cls.host}{f':{cls.port}' if cls.port else ''}/{cls.db_name}"


# class DB_SQLite:
#     filename = ':memory'
#     dialect_plus_driver = 'sqlite'

#     @classmethod
#     def get_db_url(cls):
#         return f"{DB.dialect_plus_driver}:///{cls.filename}"


DB = DB_PG
DB_URL = DB.get_db_url()
# print(DB_URL)
