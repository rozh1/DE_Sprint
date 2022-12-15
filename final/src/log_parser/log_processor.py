"""Модуль обработки данных журнала"""

from log_entity import LogEntity
import re


class LogProcessor:
    """Обработчик разобранной строки журнала.
    Собирает необходимые данные в процессе обработки"""

    def __init__(self) -> None:
        self._devices = {}
        self._users = set()
        self._log_count = 0
        self._bot_count = 0
        self._error_count = 0
        self._bad_device_name_count = 0
        self._bad_browser_name_count = 0

        self._hex_pattern = re.compile(r"\\x[0-9a-fA-F][0-9a-fA-F]")
        self._question_pattern = re.compile(r" \?+")

    def __trim_device_name(self, device: str) -> str:
        is_bad = False
        if (self._hex_pattern.search(device)):
            device = self._hex_pattern.sub("", device)
            is_bad = True

        if (self._question_pattern.search(device)):
            device = self._question_pattern.sub("", device)
            is_bad = True

        if (is_bad):
            self._bad_device_name_count += 1
        return device.strip()

    def __trim_browser_name(self, browser: str) -> str:
        is_bad = False
        if (self._hex_pattern.search(browser)):
            browser = self._hex_pattern.sub("", browser)
            is_bad = True

        if (self._question_pattern.search(browser)):
            browser = self._question_pattern.sub("", browser)
            is_bad = True

        if (is_bad):
            self._bad_browser_name_count += 1
        return browser.strip()

    def __process_device(self, log: LogEntity) -> str:
        """Обработчик устройства"""

        device = self.__trim_device_name(log.get_device())

        if (device == "Other"):
            device = log.get_os()

        if (device not in self._devices):
            self._devices[device] = {
                "use_count": 1,
                "users": set(),
                "browsers": {},
                "not_200_answers": 1 if log.get_status() != 200 else 0,
                "request_answers": {}
            }
        else:
            self._devices[device]["use_count"] += 1
            self._devices[device]["not_200_answers"] += 1 if log.get_status() != 200 else 0

        return device

    def __process_browser(self, log: LogEntity, device: str) -> None:
        """Обработчик браузера"""

        browser = self.__trim_browser_name(log.get_browser())
        browsers = self._devices[device]["browsers"]
        user = log.get_user_key()
        if (browser not in browsers):
            browsers[browser] = set([user])
        else:
            browsers[browser].add(user)

    def __process_user(self, log: LogEntity, device: str) -> None:
        """Обработчик пользователя"""

        user = log.get_user_key()

        self._users.add(user)
        self._devices[device]["users"].add(user)

    def __count_non_200_answers(self, log: LogEntity, device: str) -> None:
        """Обработчик статуса ответа"""

        if (log.get_status() == 200):
            return

        answers = self._devices[device]["request_answers"]
        if (log.get_status() in answers):
            answers[log.get_status()] += 1
        else:
            answers[log.get_status()] = 1

    def __merge_device(self, device: dict, other_device: dict) -> None:
        device["use_count"] += other_device["use_count"]
        device["not_200_answers"] += other_device["not_200_answers"]
        device["users"] = device["users"].union(other_device["users"])

        for (key, value) in other_device["browsers"].items():
            if (key in device["browsers"]):
                device["browsers"][key] = device["browsers"][key] \
                    .union(other_device["browsers"][key])
            else:
                device["browsers"][key] = value

        for (key, value) in other_device["request_answers"].items():
            if (key in device["request_answers"]):
                device["request_answers"][key] += value
            else:
                device["request_answers"][key] = value

    def process_log_entity(self, log: LogEntity) -> None:
        """Обработчик строки журнала"""

        if (log.get_device() == "Spider"):
            self._bot_count += 1

        self._log_count += 1
        device = self.__process_device(log)
        self.__process_browser(log, device)
        self.__process_user(log, device)
        self.__count_non_200_answers(log, device)

    def merge(self, other: "LogProcessor") -> None:
        """Объединение результатов с другим LogProcessor"""
        self._bot_count += other._bot_count
        self._log_count += other._log_count
        self._error_count += other._error_count
        self._bad_browser_name_count += other._bad_browser_name_count
        self._bad_device_name_count += other._bad_device_name_count
        self._users = self._users.union(other._users)

        for (key, value) in other._devices.items():
            if (key in self._devices):
                self.__merge_device(self._devices[key], value)
            else:
                self._devices[key] = value

    def set_error_count(self, error_count: int):
        """Устаналивает количество необработанных строк из журнала"""
        self._error_count = error_count

    def get_result(self) -> dict:
        """Преобразует собранные данные в результат вида:
        {
            "log_count": int - количество обработанных записей,
            "error_count": int - количество необработанных записей,
            "bot_count": int - количество роботов в журнале,
            "user_count": int - количество уникальных пользователей (IP), исключая роботов,
            "device_count": int - количество уникальных устройств,
            "bad_device_name_count": int - количество "плохих" (содержащих непечатные символы) названий устройств
            "bad_browser_name_count": int - количество "плохих" названий браузеров
            "devices": {
                "Linux": { // - название устройства или ОС
                    "use_count": int - количество записей, относящихся к устройству,
                    "use_share": float - отношение количества записей устройства ко всем записям,
                    "user_count": int - количество уникальных пользователей (IP) устройства,
                    "user_share": float - отношение количества уникальных пользователей (IP) устройства ко всем пользователям,
                    "not_200_answers": int - количество статустов ответа отличных от 200,
                    "browsers": [ // - браузеры
                        [
                            "AhrefsBot 6.1", // нзвание браузера
                            354 // количестово уникальны
                        ],
                    ],
                    "request_answers": {
                        "404": int - количество статустов ответа,
                    },
                },
            }
        }"""

        user_count = len(self._users)
        devices = {}
        for (key, value) in self._devices.items():
            devices[key] = {
                "use_count": value["use_count"],
                "use_share": value["use_count"] / self._log_count,
                "user_count": len(value["users"]),
                "user_share": len(value["users"]) / user_count,
                "not_200_answers": value["not_200_answers"],
                "request_answers": value["request_answers"]
            }
            browsers = {}
            for (browser_key, browser_value) in value["browsers"].items():
                browsers[browser_key] = len(browser_value)
            devices[key]["browsers"] = sorted(
                browsers.items(), key=lambda item: item[1], reverse=True)  # [:5]

        return {
            "log_count": self._log_count,
            "error_count": self._error_count,
            "bot_count": self._bot_count,
            "user_count": user_count,
            "bad_device_name_count": self._bad_device_name_count,
            "bad_browser_name_count": self._bad_browser_name_count,
            "device_count": len(devices),
            "devices": devices
        }
