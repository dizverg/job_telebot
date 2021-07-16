import logging

LOG = {'format': "%(asctime)s - [%(levelname)s] - %(name)s - "
                 "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
       'level': logging.INFO}


class DB:
    filename = 'job_telebot.db'
    db_name = 'job_telebot'
    user = 'postgres'
    password = 'lid7Ohch3e'
    host = 'localhost'
    port = None
    dialect_plus_driver = 'postgresql+psycopg2'


DB_URL = f"{DB.dialect_plus_driver}://{DB.user}" \
         f"{f':{DB.password}' if DB.password else ''}@" \
         f"{DB.host}{f':{DB.port}' if DB.port else ''}/{DB.db_name}"
