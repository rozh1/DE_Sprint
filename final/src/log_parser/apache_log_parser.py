"""Модуль разбора файлов журнала Apache 2.4"""

import os
import sys
import re
import typing
from log_entity import LogEntity
from dateutil.parser import parse as date_parse


class ApacheLogParser:
    """Модуль разбора файлов журнала Apache 2.4

    Выполняет рабор строки журнала, записанной в формате
        40.77.167.129 - - [22/Jan/2019:03:56:17 +0330] "GET /image/23488/productModel/150x150 HTTP/1.1" 200 2654 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)" "-"
        формат соответсвует конфигурации журнала Apache: "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"",
        где:
            %h - IP клиента
            %l - "-" в выводе указывает на то, что часть запрошенной информации недоступна.
            %u - Пользователь, если авторизовался
            %t - время запроса
            \"%r\" - запрос, адрес, протокол
            %>s - код результата ответа
            %b - размер ответа
            \"%{Referer}i\" - источник запроса
            \"%{User-agent}i\" - идентикатор браузера

    Выдает данные построчно как итерируемый объект
    """

    def __init__(self) -> None:
        self.error_count = 0
        self._regex = re.compile("^(?P<IP>\S*)\s(?P<I>.)\s(?P<User>\S*)\s\[(?P<Time>.*)\]\s\"(?P<Method>\S*)\s" +
                                 "(?P<Address>\S*)\s(?P<Protocol>[^\"]*)\"\s(?P<Status>\S*)\s(?P<Size>\S*)\s" +
                                 "\"(?P<Referrer>[^\"]*)\"\s\"(?P<UA>[^\"]*)\"\s\"(?P<Addition>[^\"]*)\"$") \
                        .match

    def __parse_line(self, line: str) -> LogEntity:
        """Выполняет рабор строки журнала, записанной в заданном формате"""

        match = self._regex(line)

        ip = match.group("IP")
        full_info = match.group("I") != "-"
        user = match.group("User")
        time = match.group("Time")
        method = match.group("Method")
        address = match.group("Address")
        protocol = match.group("Protocol")
        status = int(match.group("Status"))
        size = int(match.group("Size"))
        referrer = match.group("Referrer")
        user_agent = match.group("UA")
        addition = match.group("Addition")

        if (user == "-"):
            user = ""

        # 22/Jan/2019:03:56:17 +0330 -> 22/Jan/2019 03:56:17 +0330
        time = date_parse(time[:11] + " " + time[12:])
        time = time.timestamp() # время в формате unix timestamp (int)

        return LogEntity(ip, full_info, user, time, method, address, protocol, status, size, referrer, user_agent, addition)

    def parse(self, file_path: str, chunk_number: int = 1, chunk_count: int = 1) -> typing.Iterator[LogEntity]:
        """Выполняет разбор файла журнанала Apache 2.4"""

        file_size = os.path.getsize(file_path)
        start = file_size / chunk_count * (chunk_number-1)
        end = start + file_size / chunk_count
        with open(file_path, "r") as log_file:
            if (start != 0):
                # если мы попадем на следующий символ после \n (новая строка),
                # то будет выполнен пропуск строки, поэтому start-1
                log_file.seek(start-1)
                # читаем и пропускаем первую (неполную строку) и пропускаем ее
                chunk_correct = log_file.readline()
                start += len(chunk_correct)

            for log_line in log_file:
                try:
                    yield self.__parse_line(log_line)
                except Exception as exception:
                    print(exception, file=sys.stderr)
                    print(log_line, file=sys.stderr)
                    self.error_count += 1

                readed_bytes = len(log_line)
                start += readed_bytes
                if (start >= end):
                    break


if __name__ == "__main__":
    parser = ApacheLogParser()
    for p in parser.parse(r"/media/share/DE/logs/access.log", 2, 100):
        pass
