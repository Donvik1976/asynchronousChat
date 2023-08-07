"""Сервер"""

import sys
import os
import argparse
import logs.logs_config.server_log_config
import configparser
from logging import getLogger
from common.utils import *
from server.core import MessageProcessor
from server.database import ServerStorage
from server.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Инициализация логирования сервера.
logger = getLogger('server')


def log(func_to_log):
    def log_saver(*args, **kwargs):
        logger.debug(
            f'Была вызвана функция {func_to_log.__name__} '
            f'c параметрами {args}, {kwargs}. '
            f'Вызов из модуля {func_to_log.__module__}')
        ret = func_to_log(*args, **kwargs)
        return ret

    return log_saver


# Парсер аргументов коммандной строки.
@log
def arg_parser(default_port, default_address):
    '''
    Парсинг аргументов командной строки для конфигурации приложения.
    Эта функция использует argparse для разбора аргументов командной строки,
    предоставляемых при запуске приложения. Она позволяет пользователю указать
    параметры, такие как адрес слушания, порт слушания и флаг использования
    графического интерфейса (GUI), с помощью опций командной строки.
    Параметры:
        default_port (int): Значение по умолчанию для порта слушания, если не
        указано пользователем.
        default_address (str): Значение по умолчанию для адреса слушания, если
        не указано пользователем.
    Опции командной строки:
        -p (int, optional): Порт слушания. Если не указан, будет использовано
        значение default_port.
        -a (str, optional): Адрес слушания. Если не указан, будет использовано
        значение default_address.
        --no_gui (flag): Флаг отключения графического интерфейса. Если указан,
        приложение запускается без GUI.
    Возвращает:
        tuple: Кортеж, содержащий следующие элементы:
            listen_address (str): Адрес слушания для приложения.
            listen_port (int): Порт слушания для приложения.
            gui_flag (bool): Флаг использования графического интерфейса.
            True, если GUI отключен (--no_gui).
    Пример:
        При запуске приложения с командной строкой:
        $ python app.py -p 8080 -a 192.168.0.100 --no_gui
        Вызов функции arg_parser() вернет кортеж:
        ('192.168.0.100', 8080, True)
    '''
    logger.debug(
        f'Инициализация парсера аргументов коммандной строки: {sys.argv}')
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('--no_gui', action='store_true')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    gui_flag = namespace.no_gui
    logger.debug('Аргументы успешно загружены.')
    return listen_address, listen_port, gui_flag


@log
# Загрузка файла конфигурации
def config_load():
    '''
    Загрузка файла конфигурации или создание нового файла с настройками по
    умолчанию.
    Эта функция загружает конфигурационный файл 'server.ini' с помощью
    configparser.
    Если файл загружен успешно и содержит раздел 'SETTINGS', функция
    возвращает объект configparser.ConfigParser с загруженными настройками.
    '''
    config = configparser.ConfigParser()
    dir_path = os.getcwd()
    config.read(f"{dir_path}/{'server.ini'}")
    # Если конфиг файл загружен правильно, запускаемся, иначе по умолчанию.
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', '')
        config.set('SETTINGS', 'Database_file', 'server_database.db3')
        return config


@log
def main():
    '''
    Главная функция для запуска серверного приложения.
    Логика работы:
        1. Загружается конфигурационный файл сервера с помощью функции
        config_load().
        2. Загружаются параметры командной строки с помощью функции
        arg_parser().
        3. Инициализируется база данных сервера с помощью ServerStorage.
        4. Создается экземпляр класса MessageProcessor для обработки сообщений,
         и сервер запускается.
        5. Если указан параметр без GUI, сервер работает в режиме простого
        обработчика консольного ввода. Ввод команды 'exit' завершает основной
        цикл сервера.
        6. Если не указан запуск без GUI, сервер запускается с графическим
        интерфейсом:
           - Создается объект QApplication.
           - Создается графическое окружение (MainWindow) для сервера,
           используя базу данных, экземпляр MessageProcessor и конфигурацию.
           - Запускается GUI с помощью server_app.exec_().
           - По закрытию окон, обработчик сообщений (server) останавливается
           (server.running = False).
    '''

    # Загрузка файла конфигурации сервера
    config = config_load()

    """
    Загрузка параметров командной строки, если нет параметров, то задаём 
    значения по умоланию.
    """
    listen_address, listen_port, gui_flag = arg_parser(
        config['SETTINGS']['Default_port'],
        config['SETTINGS']['Listen_Address'])
    # Инициализация базы данных
    database = ServerStorage(
        os.path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file']))

    # Создание экземпляра класса - сервера и его запуск:
    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    # Если указан параметр без GUI, то запускаем простенький обработчик
    # консольного ввода
    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера.')
            if command == 'exit':
                # Если выход, то завршаем основной цикл сервера.
                server.running = False
                server.join()
                break

    # Если не указан запуск без GUI, то запускаем GUI:
    else:
        # Создаём графическое окружение для сервера:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)

        # Запускаем GUI
        server_app.exec_()

        # По закрытию окон останавливаем обработчик сообщений
        server.running = False


if __name__ == '__main__':
    main()
