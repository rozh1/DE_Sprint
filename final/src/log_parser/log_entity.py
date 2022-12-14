"""Модуль представления данных строки журнала"""

from user_agents import parse


class LogEntity:
    """Представление строки журнала как объекта"""

    def __init__(self, ip: str, full_info: bool, user: str, time: int, method: str,
                 address: str, protocol: str, status: int, size: int, referrer: str,
                 user_agent: str, addition: str) -> None:

        self._ip = ip
        self._full_info = full_info
        self._user = user
        self._time = time
        self._method = method
        self._address = address
        self._protocol = protocol
        self._status = status
        self._size = size
        self._referrer = referrer
        self._user_agent = user_agent
        self._addition = addition
        self._ua = parse(self._user_agent)

    def get_status(self) -> int:
        """Получить статус запроса"""
        return self._status

    def get_user_key(self) -> str:
        """Получить идентификатор пользователя"""
        return " ".join((self._ip, self._user))

    def get_device(self) -> str:
        """Получить название устройства"""
        device = self._ua.device
        return device.family if device.family is not None else "" + \
            " " + device.brand if device.brand is not None else "" + \
            " " + device.model if device.model is not None else ""

    def get_browser(self) -> str:
        """Получить название браузера и его вресию"""
        browser = self._ua.browser
        return (browser.family if browser.family is not None else "") + " " + (browser.version_string if browser.version_string is not None else "")

    def get_os(self) -> str:
        """Получить название ОС и ее вресию"""
        os = self._ua.os
        return (os.family if os.family is not None else "") + " " + (os.version_string if os.version_string is not None else "")
