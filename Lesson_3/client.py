"""Клиент"""
import json
import sys
import socket

import time
from common.utils import get_message, send_message
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, DEFAULT_PORT, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_IP_ADRESS


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
    return out


def process_ans(message):
    '''
    Функция разбирает ответ сервера
    :param message: словарь ответа сервера
    :return: строка с описанием ответа
    '''
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    '''
    Загружаем параметры коммандной строки

    '''
    # client.py 192.168.57.33 8079
    # server.py -p 8079 -a 192.168.0.102
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print(
            'В качестве порта может быть указано только число в диапазоне от 1021 до 65535')
        sys.exit()

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    # {'action': 'presence', 'time': ....., 'user': {'account_name': 'Guest'}}
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()



