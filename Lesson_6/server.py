"""Серверная часть"""

import argparse
import json
import logging
import traceback

import logs.logs_config.server_log_config
import socket
import sys

from common.utils import get_message, send_message
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from errors import IncorrectDataRecivedError

#Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')


def log(func):
    """Функция декоратор"""

    def log_wrapper(*args, **kwargs):
        """Обертка"""

        ret = func(*args, **kwargs)
        SERVER_LOGGER.debug(
            f'Вызвана функция {func.__name__} с параметрами {args},{kwargs}'
            f'Из модуля {func.__module__}'
            f'Из функции {traceback.format_stack()[0].strip().split()[-1]}')
        return ret

    return log_wrapper

@log
def process_client_message(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message: словарь сообщения от клиента
    :return: словарь ответа для клиента
    '''
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    # {'action': 'presence', 'time': ....., 'user': {'account_name': 'Guest'}}
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
        and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def create_arg_parser():
    """
    Парсер аргументов коммандной строки
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser



def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаем по умолчанию
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.0.102

    '''
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')
    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_cient = get_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение {message_from_cient}')
            response = process_client_message(message_from_cient)
            SERVER_LOGGER.info(f'Cформирован ответ клиенту {response}')
            send_message(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать JSON строку, полученную от '
                                f'клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataRecivedError:
            SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                                f'Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
