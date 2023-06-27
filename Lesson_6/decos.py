import inspect
import traceback
import logging
import sys

import logs.logs_config.client_log_config
import logs.logs_config.server_log_config


if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def log(func):
    """Функция декоратор"""

    def log_wrapper(*args, **kwargs):
        """Обертка"""

        ret = func(*args, **kwargs)
        LOGGER.debug(
            f'Вызвана функция {func.__name__} с параметрами {args},{kwargs}'
            f'Из модуля {func.__module__}'
            f'Из функции {traceback.format_stack()[0].strip().split()[-1]}'
            f'Или из функции{inspect.stack()[1][3]}', stacklevel=2)
        return ret

    return log_wrapper


class Log:
    """Класс-декоратор"""

    def __call__(self, func):
        def log_wrapper(*args, **kwargs):
            """Обертка"""
            ret = func(*args, **kwargs)
            LOGGER.debug(
                f'Вызвана функция {func.__name__} с параметрами {args},{kwargs}'
                f'Из модуля {func.__module__}'
                f'Из функции {traceback.format_stack()[0].strip().split()[-1]}'
                f'Или из функции{inspect.stack()[1][3]}', stacklevel=2)
            return ret

        return log_wrapper
