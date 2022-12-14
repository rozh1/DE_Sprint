"""
Программа формирования витрины данных

Входные параметры:
    - путь к файлу результата разбора лога
"""

import sys
import json
from pg_data_mart import PgDataMart

HELP_MSG = '''
Использование: main.py /home/admin/result.json 4
    /var/log/apache2/access.log - путь к файлу результата разбора лога
    '''


def get_common_params(data: dict) -> tuple:
    """Получить данные для общих параметров"""

    return (
        ("log_count", data["log_count"]),
        ("error_count", data["error_count"]),
        ("bot_count", data["bot_count"]),
        ("user_count", data["user_count"]),
    )


def get_devices(data: dict) -> tuple:
    """Получить общие данные для устройств"""

    result = []
    counter = 1
    for (key, value) in data["devices"].items():
        result.append(
            (counter, key,
             value["use_count"], value["user_count"],
             value["not_200_answers"]))
        counter += 1
    return result


def load_request_answers(db: PgDataMart, data: dict) -> tuple:
    """Загрузить количество ответов, отличных от 200"""

    counter = 1
    for (_, value) in data["devices"].items():
        result = []
        for code, count in value["request_answers"].items():
            result.append((counter, int(code), count))
        counter += 1
        if (len(result) > 0):
            db.load_answers_data(result)

def load_browsers(db: PgDataMart, data: dict) -> tuple:
    """Загрузить данные о браузерах с привязкой к устройству в БД"""

    counter = 1
    for (_, value) in data["devices"].items():
        result = []
        for browser in value["browsers"]:
            result.append((counter, browser[0], browser[1]))
        counter += 1
        if (len(result) > 0):
            db.load_browsers(result)


def process_data(data: dict):
    """Загрузка данных в БД"""

    with PgDataMart() as pg:
        pg.create_schema()
        pg.load_common_data(get_common_params(data))
        pg.load_devices(get_devices(data))
        load_request_answers(pg, data)
        load_browsers(pg, data)


if __name__ == "__main__":

    with open("result.json", "r") as input:
        process_data(json.load(input))
    if (len(sys.argv) < 2):
        print(HELP_MSG)
        sys.exit(-1)

    with open(sys.argv[1], "r") as input:
        process_data(json.load(input))
