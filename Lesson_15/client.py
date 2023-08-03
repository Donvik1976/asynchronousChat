"""Клиент"""

import logs.logs_config.client_log_config
import argparse
import sys
import os
from logging import getLogger
from Crypto.PublicKey import RSA
from PyQt5.QtWidgets import QApplication, QMessageBox

from common.variables import *
from common.errors import ServerError
from client.database import ClientDatabase
from client.transport import ClientTransport
from client.main_window import ClientMainWindow
from client.start_dialog import UserNameDialog

# Инициализация клиентского логера
logger = getLogger('client')


def log(func_to_log):
    def log_saver(*args, **kwargs):
        logger.debug(
            f'Была вызвана функция {func_to_log.__name__} '
            f'c параметрами {args}, {kwargs}. '
            f'Вызов из модуля {func_to_log.__module__}')
        ret = func_to_log(*args, **kwargs)
        return ret

    return log_saver


# Парсер аргументов коммандной строки
@log
def arg_parser():
    '''
    Парсинг аргументов командной строки для настройки параметров клиента.
    Эта функция использует argparse для анализа аргументов командной строки,
    предоставляемых при запуске скрипта клиента. Она позволяет пользователю
    указать адрес сервера, порт сервера, имя клиента и пароль клиента с
    помощью опций командной строки.
    Опции командной строки:
        addr (str, optional): IP-адрес сервера для подключения. Если не указан,
        будет использован адрес по умолчанию.
        port (int, optional): Номер порта на сервере для подключения. Если не
        указан, будет использован порт по умолчанию.
        -n, --name (str, optional): Имя для идентификации клиента. Если не
        указано, имя не будет задано.
        -p, --password (str, optional): Пароль для аутентификации на сервере.
        Если не указан, будет использован пустой пароль.
    Возвращает:
        tuple: Кортеж, содержащий следующие элементы:
            server_address (str): IP-адрес сервера для подключения.
            server_port (int): Номер порта на сервере для подключения.
            client_name (str): Имя для идентификации клиента.
            client_passwd (str): Пароль для аутентификации на сервере.
    Вызывает:
        SystemExit: Если указанный номер порта сервера не находится в
        допустимом диапазоне (1024 до 65535), функция записывает сообщение об
        ошибке и завершает работу клиента.
    Пример:
        Запуск клиента с пользовательскими настройками:
        $ python client.py 192.168.0.100 8080 -n Alice -p pass123
        Запуск клиента с настройками по умолчанию:
        $ python client.py
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    client_passwd = namespace.password

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)

    return server_address, server_port, client_name, client_passwd


# Основная функция клиента
if __name__ == '__main__':
    '''
    Основная точка входа в клиентское приложение.
    При запуске этого модуля как самостоятельного скрипта (не импортируясь 
    как модуль), выполняется код внутри этого блока.
    Параметры командной строки:
        При запуске приложения, функция arg_parser() используется для разбора 
        аргументов командной строки и получения значений 
        server_address, server_port, client_name и client_passwd.
    Логика работы:
        1. Загружаются параметры командной строки с помощью arg_parser() и 
        инициализируется логирование.
        2. Создается экземпляр QApplication для графического интерфейса.
        3. Если имя пользователя (client_name) или пароль (client_passwd) не 
        были указаны в командной строке, открывается диалоговое окно 
        (UserNameDialog) для их ввода.
        4. Если пользователь ввел имя и нажал "ОК", то сохраняем введенное имя 
        и пароль.
        5. Записываются логи о запущенном клиенте с указанными параметрами.
        6. Загружаются ключи из файла, если файл не существует, то 
        генерируется новая пара ключей RSA.
        7. Создается объект базы данных (ClientDatabase) для хранения 
        сообщений.
        8. Создается объект-транспорт (ClientTransport) и запускается 
        транспортный поток.
        9. Создается графический интерфейс (ClientMainWindow), подключается к 
        транспорту и запускается.
        10. При закрытии графической оболочки, транспорт закрывается и 
        выполняется ожидание завершения его работы.
    '''
    # Загружаем параметы коммандной строки
    server_address, server_port, client_name, client_passwd = arg_parser()
    logger.debug('Args loaded')

    # Создаём клиентокое приложение
    client_app = QApplication(sys.argv)

    # Если имя пользователя не было указано в командной строке то запросим его
    start_dialog = UserNameDialog()
    if not client_name or not client_passwd:
        client_app.exec_()
        # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое и
        # удаляем объект, инааче выходим
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_passwd = start_dialog.client_passwd.text()
            logger.debug(
                f'Using USERNAME = {client_name}, PASSWD = {client_passwd}.')
        else:
            exit(0)

    # Записываем логи
    logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
        f'порт: {server_port}, имя пользователя: {client_name}')

    # Загружаем ключи с файла, если же файла нет, то генерируем новую пару.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    key_file = os.path.join(dir_path, f'{client_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    # !!!keys.publickey().export_key()
    logger.debug("Keys sucsessfully loaded.")
    # Создаём объект базы данных
    database = ClientDatabase(client_name)
    # Создаём объект - транспорт и запускаем транспортный поток
    try:
        transport = ClientTransport(
            server_port,
            server_address,
            database,
            client_name,
            client_passwd,
            keys)
        logger.debug("Transport ready.")
    except ServerError as error:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', error.text)
        exit(1)
    transport.setDaemon(True)
    transport.start()

    # Удалим объект диалога за ненадобностью
    del start_dialog

    # Создаём GUI
    main_window = ClientMainWindow(database, transport, keys)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат Программа alpha release - {client_name}')
    client_app.exec_()

    # Раз графическая оболочка закрылась, закрываем транспорт
    transport.transport_shutdown()
    transport.join()
