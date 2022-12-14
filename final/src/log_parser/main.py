"""
Программа разбора логов для web-сервера Apache 2.4

Входные параметры:
    - путь к файлу лога
    - путь к файлу результата
"""

import sys
import json
from multiprocessing import Pool
from apache_log_parser import ApacheLogParser
from log_processor import LogProcessor

HELP_MSG = '''
Использование: main.py /var/log/apache2/access.log /home/admin/result.json 4
    /var/log/apache2/access.log - путь к файлу лога
    /home/admin/result.json - путь к файлу результата
    4 - количество параллельных обработчиков
    '''


def process_file(log_file: str, chunk_number: int, chunk_count: int) -> LogProcessor:
    processor = LogProcessor()
    parser = ApacheLogParser()
    for log in parser.parse(log_file, chunk_number, chunk_count):
        processor.process_log_entity(log)

    processor.set_error_count(parser.error_count)
    return processor


def process_log(log_file: str, result_file: str, parallel: int = 1):
    """Обработчик журнала
    log_file - путь к файлу журнала    
    result_file - путь для записи результата в формате json
    """
    process_args = []

    for n in range(1, parallel+1):
        process_args.append((log_file, n, parallel))

    processors = []
    with Pool(processes=parallel) as pool:
        processors = pool.starmap(process_file, process_args)

    main_processor = processors[0]
    for i in range(1, parallel):
        main_processor.merge(processors[i])

    result = main_processor.get_result()

    with open(result_file, "w") as out:
        out.write(json.dumps(result, indent=4))


if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print(HELP_MSG)
        sys.exit(-1)

    process_log(sys.argv[1], sys.argv[2], int(
        sys.argv[3]) if len(sys.argv) > 3 else 1)
