"""
Файл облегчающий запуск серверной части и любого числа клиентов
"""

import subprocess

PROCESS = []


while True:
    ANSWER = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ANSWER == 'q':
        break
    elif ANSWER == 's':
        clients_count = int(input('Введите количество клиентов для запуска: '))
        PROCESS.append(
            subprocess.Popen('python server.py',
                             creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(clients_count):
            PROCESS.append(
                subprocess.Popen(f'python client.py -n test{i + 1}',
                                 creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ANSWER == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
