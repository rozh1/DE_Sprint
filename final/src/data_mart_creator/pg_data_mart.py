"""Модуль доступа к витрине данных Postgres"""

import config
import psycopg2
from psycopg2 import sql


_DEVICES_TABLE_DROP_QUERY = """DROP TABLE IF EXISTS public.devices;"""
_DEVICES_TABLE_CREATE_QUERY = """CREATE TABLE public.devices
(
    id serial,
    name character varying NOT NULL,
    use_count integer NOT NULL,
    user_count integer NOT NULL,
    not_200_answers integer NOT NULL,
    PRIMARY KEY (id)
);"""
_DEVICES_TABLE_INSERT_QUERY_FMT = """INSERT INTO public.devices (id, name, use_count, user_count, not_200_answers) VALUES {}"""

_COMMON_TABLE_DROP_QUERY = """DROP TABLE IF EXISTS public.common_parameters;"""
_COMMON_TABLE_CREATE_QUERY = """CREATE TABLE public.common_parameters
(
    name character varying NOT NULL,
    value integer NOT NULL,
    PRIMARY KEY (name)
);"""
_COMMON_TABLE_INSERT_QUERY_FMT = """INSERT INTO public.common_parameters (name, value) VALUES {}"""


_ANSWERS_TABLE_DROP_QUERY = """DROP TABLE IF EXISTS public.answer_statistics;"""
_ANSWERS_TABLE_CREATE_QUERY = """CREATE TABLE public.answer_statistics
(
    device_id integer NOT NULL,
    code integer NOT NULL,
    count integer,
    PRIMARY KEY (device_id, code)
);"""
_ANSWERS_TABLE_INSERT_QUERY_FMT = """INSERT INTO public.answer_statistics (device_id, code, count) VALUES {}"""


_BROWSERS_TABLE_DROP_QUERY = """DROP TABLE IF EXISTS public.browsers;"""
_BROWSERS_TABLE_CREATE_QUERY = """CREATE TABLE public.browsers
(
    device_id integer NOT NULL,
    browser_name character varying NOT NULL,
    user_count integer,
    PRIMARY KEY (device_id, browser_name)
);"""
_BROWSERS_TABLE_INSERT_QUERY_FMT = """INSERT INTO public.browsers (device_id, browser_name, user_count) VALUES {}"""

class PgDataMart:
    """Реализация загрузчика для Postgres"""
    
    def __init__(self) -> None:
        self.connection = psycopg2.connect(
            dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD, host=config.DB_HOST)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.close()

    def create_schema(self) -> None:
        """Создать схему данных"""

        with self.connection.cursor() as cursor:
            cursor.execute(_DEVICES_TABLE_DROP_QUERY)
            cursor.execute(_COMMON_TABLE_DROP_QUERY)
            cursor.execute(_ANSWERS_TABLE_DROP_QUERY)
            cursor.execute(_BROWSERS_TABLE_DROP_QUERY)

            cursor.execute(_DEVICES_TABLE_CREATE_QUERY)
            cursor.execute(_COMMON_TABLE_CREATE_QUERY)
            cursor.execute(_ANSWERS_TABLE_CREATE_QUERY)
            cursor.execute(_BROWSERS_TABLE_CREATE_QUERY)

            self.connection.commit()

    def __load_data(self, fmt: str, values: tuple):
        with self.connection.cursor() as cursor:
            insert = sql.SQL(fmt).format(
                sql.SQL(',').join(map(sql.Literal, values)))
            cursor.execute(insert)
            self.connection.commit()

    def load_common_data(self, values: tuple) -> None:
        """Загрузить общие данные"""

        self.__load_data(_COMMON_TABLE_INSERT_QUERY_FMT, values)

    def load_answers_data(self, values: tuple) -> None:
        """Загрузить данные ответов, отличных от 200"""

        self.__load_data(_ANSWERS_TABLE_INSERT_QUERY_FMT, values)

    def load_devices(self, values: tuple) -> None:
        """Загрузить данные о устройствах"""

        self.__load_data(_DEVICES_TABLE_INSERT_QUERY_FMT, values)

    def load_browsers(self, values: tuple) -> None:
        """Загрузить данные о браузерах"""

        self.__load_data(_BROWSERS_TABLE_INSERT_QUERY_FMT, values)


if __name__ == "__main__":
    with PgDataMart() as pg:
        pg.create_schema()
