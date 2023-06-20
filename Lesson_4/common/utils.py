"""Утилиты"""
import json

from common.variables import МAX_PACKAGE_LENGTH, ENCODING


def get_message(sock):
    '''
    Утилита преёма и декорирования сообщения
    принимает байты выдаёт словарь, если принято что-то другое отдаёт ошибку
     значения
    :param sock: сокет для получения сообщения
    :return: словарь с сообщением
    '''

    encoded_response = sock.recv(МAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(sock, message):
    '''
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его
    :param sock: сокет для отправки сообщения
    :param message: словарь с сообщением
    '''

    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
