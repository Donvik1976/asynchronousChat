"""Логи Сервера"""

import sys
import os

from logging import Formatter, StreamHandler, handlers, getLogger, ERROR
from common.variables import LOGGING_LEVEL

# создаём формировщик логов
SERVER_FORMATTER = Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s'
)

# Подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, '../logs_files/server.log')

# создаём потоки вывода логов
STREAM_HANDLER = StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(ERROR)
LOG_FILE = handlers.TimedRotatingFileHandler(
    PATH, encoding='utf8', interval=1, when='m'
)
LOG_FILE.setFormatter(SERVER_FORMATTER)

# создаём регистратор и настраиваем его
LOGGER = getLogger('server')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info("Информационное сообщение")
