import logging, sys
from private_token import tokens

MODE =sys.argv[1] if len(sys.argv)>1 else None
TOKEN =tokens.get(MODE or list(tokens)[0])

LOG = {'format': "%(asctime)s - [%(levelname)s] - %(name)s - "
                 "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
       'level': logging.INFO}

CHANEL_ID = -1001568792005

class DB_PG:
    filename = 'job_telebot.db'
    db_name = 'job_telebot'
    user = 'postgres'
    password = 'lid7Oadsh'
    host = 'localhost'
    port = None
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

