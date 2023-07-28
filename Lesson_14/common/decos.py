import socket
import logging
import logs.logs_config.client_log_config
import logs.logs_config.server_log_config
import sys

sys.path.append('../')

# метод определения модуля, источника запуска.
if sys.argv[0].find('client') == -1:
    #если не клиент то сервер!
    logger = logging.getLogger('server')
else:
    # ну, раз не сервер, то клиент
    logger = logging.getLogger('client')


def log(func_to_log):
    def log_saver(*args, **kwargs):
        logger.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args} , {kwargs}. Вызов из модуля {func_to_log.__module__}')
        ret = func_to_log(*args, **kwargs)
        return ret
    return log_saver


def login_required(func):
    '''
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    '''

    def checker(*args, **kwargs):
        # проверяем, что первый аргумент - экземпляр MessageProcessor
        # Импортить необходимо тут, иначе ошибка рекурсивного импорта.
        from server.core import MessageProcessor
        from common.variables import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса
                    # MessageProcessor
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence
            # сообщение. Если presense, то разрешаем
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            # Если не не авторизован и не сообщение начала авторизации, то
            # вызываем исключение.
            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker


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
