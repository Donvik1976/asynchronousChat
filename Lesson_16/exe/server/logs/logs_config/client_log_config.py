"""Логи Клиента"""

import sys
import os

from logging import Formatter, StreamHandler, ERROR, FileHandler, getLogger
from common.variables import LOGGING_LEVEL

# создаём формировщик логов
CLIENT_FORMATTER = Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s'
)

# Подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, '../logs_files/client.log')

# создаём потоки вывода логов
STREAM_HANDLER = StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
STREAM_HANDLER.setLevel(ERROR)
LOG_FILE = FileHandler(PATH, encoding='utf8')
LOG_FILE.setFormatter(CLIENT_FORMATTER)

# создаём регистратор и настраиваем его
LOGGER = getLogger('client')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info("Информационное сообщение")
