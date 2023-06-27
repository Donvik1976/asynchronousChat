"""Клиент"""

import argparse
import json
import logging
import sys
import socket
import time
import traceback

import logs.logs_config.client_log_config
from errors import ReqFieldMissingError
from common.utils import get_message, send_message
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, DEFAULT_PORT, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_IP_ADRESS


# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')

class Log:
    """Класс-декоратор"""

    def __call__(self, func):
        def log_wrapper(*args, **kwargs):
            """Обертка"""
            ret = func(*args, **kwargs)
            # Инициализация клиентского логера
            CLIENT_LOGGER.debug(
                f'Вызвана функция {func.__name__} с параметрами {args},{kwargs}'
                f'Из модуля {func.__module__}'
                f'Из функции {traceback.format_stack()[0].strip().split()[-1]}')
            return ret

        return log_wrapper

@Log()
def create_presence(account_name='Guest'):
    '''
    Сообщение о присутствии
    :param account_name: имя аккаунта (по умолчанию 'Guest')
    :return: словарь сообщения о присутствии
    '''
    # {'action': 'presence', 'time': ....., 'user': {'account_name': 'Guest'}}
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out

@Log()
def process_ans(message):
    '''
    Функция разбирает ответ сервера
    :param message: словарь ответа сервера
    :return: строка с описанием ответа
    '''
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


def create_arg_parser():
    """
    Создаём парсер аргументов коммандной строки
    :return: объект парсера аргументов
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser


def main():
    """
    Загружаем параметры коммандной строки
    """
    # client.py 192.168.57.33 8079
    # server.py -p 8079 -a 192.168.0.102
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address}, порт: {server_port}')

    # Инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        message_to_server = create_presence()
        send_message(transport, message_to_server)
        answer = process_ans(get_message(transport))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()



