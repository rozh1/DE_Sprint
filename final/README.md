# Cкрипт для формирования витрины на основе логов web-сайта

## Задача

Разработать скрипт формирования витрины следующего содержания:

1. Суррогатный ключ устройства
1. Название устройства
1. Количество пользователей
1. Доля пользователей данного устройства от общего числа пользователей.
1. Количество совершенных действий для данного устройства
1. Доля совершенных действий с данного устройства, относительно других устройств
1. Список из 5 самых популярных браузеров, используемых на данном устройстве различными пользователями, с указанием доли использования для данного браузера относительно остальных браузеров.
1. Количество ответов сервера отличных от 200 на данном устройстве
1. Для каждого из ответов сервера, отличных от 200, сформировать поле, в котором будет содержаться количество ответов данного типа

## Использование скрипта

Установка зависимостей:

```
pip install -r ./src/requirements.txt
```

Запуск скрипта разбора:

```
python3 ./src/log_parser/main.py /var/log/apache2/access.log /home/admin/result.json 4
```

Здесь:

* `/var/log/apache2/access.log` - путь к файлу лога
* `/home/admin/result.json` - путь к файлу результата
* `4` - количество параллельных обработчиков

Запуск скрипта формирования витрины данных:

```
python3 ./src/data_mart_creator/main.py /home/admin/result.json
```

Здесь:

* `/home/admin/result.json` - путь к файлу результата

Конфигурация подключения к БД (файл `src/data_mart_creator/config.py`):

```
DB_NAME = "ApacheLog" # Имя БД
DB_USER = "postgres" # пользователь БД
DB_PASSWORD = "postgres" # пароль БД
DB_HOST = "localhost" # адрес сервера БД
```

## Формирование витрины данных

Все данные для формирования витринных данных доступы в JSON файл результата обработки лога. При необходимости возможно получение данных их БД с помощью запроса:

```
SELECT ID,
	NAME,
	USE_COUNT,
	USE_COUNT /
	(SELECT VALUE
		FROM PUBLIC.COMMON_PARAMETERS
		WHERE NAME = 'log_count') AS USE_SHARE,
	USER_COUNT,
	USER_COUNT /
	(SELECT VALUE
		FROM PUBLIC.COMMON_PARAMETERS
		WHERE NAME = 'user_count') AS USER_SHARE,
	NOT_200_ANSWERS,
	ARRAY
	(SELECT BROWSER_NAME
		FROM PUBLIC.BROWSERS
		WHERE DEVICE_ID = ID
		ORDER BY USER_COUNT DESC
		LIMIT 5) AS BROWSERS,
	ARRAY
	(SELECT CODE || ': ' || COUNT
		FROM PUBLIC.ANSWER_STATISTICS
		WHERE DEVICE_ID = ID
		ORDER BY COUNT DESC) AS ANSWERS
FROM PUBLIC.DEVICES;
```

Здесь:

* `ID` - Id устройства
* `NAME` - Название устройства
* `USER_COUNT` - Количество пользователей
* `USER_SHARE` - Доля пользователей данного устройства от общего числа пользователей
* `USE_COUNT` - Количество совершенных действий для данного устройства
* `USE_SHARE` - Доля совершенных действий с данного устройства, относительно других устройств
* `BROWSERS` - Список из 5 самых популярных браузеров, используемых на данном устройстве различными пользователями, с указанием доли использования для данного браузера относительно остальных браузеров
* `NOT_200_ANSWERS` - Количество ответов сервера отличных от 200 на данном устройстве
* `ANSWERS` - Количество всех ответов, отличных от 200
