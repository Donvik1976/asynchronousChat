"""Утилиты"""
import json

from common.variables import *


def get_message(sock):
    '''
    Утилита преёма и декорирования сообщения
    принимает байты выдаёт словарь, если принято что-то другое отдаёт ошибку
     значения
    :param sock: сокет для получения сообщения
    :return: словарь с сообщением
    '''

    encoded_response = sock.recv(MAX_PACKAGE_LENGTH)
    json_response = encoded_response.decode(ENCODING)
    response = json.loads(json_response)
    if isinstance(response, dict):
        return response
    else:
        raise TypeError


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
