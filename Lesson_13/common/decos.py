import sys
import logs.logs_config.server_log_config
import logs.logs_config.client_log_config
import logging

# метод определения модуля, источника запуска.
if sys.argv[0].find('client') == -1:
    #если не клиент то сервер!
    logger = logging.getLogger('server')
else:
    # ну, раз не сервер, то клиент
    logger = logging.getLogger('client')


def log(func_to_log):
    def log_saver(*args , **kwargs):
        logger.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args} , {kwargs}. Вызов из модуля {func_to_log.__module__}')
        ret = func_to_log(*args , **kwargs)
        return ret
    return log_saver

# class Log:
#     """Класс-декоратор"""
#
#     def __call__(self, func):
#         def log_wrapper(*args, **kwargs):
#             """Обертка"""
#             ret = func(*args, **kwargs)
#             LOGGER.debug(
#                 f'Вызвана функция {func.__name__} с параметрами {args},{kwargs}'
#                 f'Из модуля {func.__module__}'
#                 f'Из функции {traceback.format_stack()[0].strip().split()[-1]}'
#                 f'Или из функции{inspect.stack()[1][3]}', stacklevel=2)
#             return ret
#
#         return log_wrapper
