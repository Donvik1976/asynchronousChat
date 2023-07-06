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
        PROCESS.append(
            subprocess.Popen('python server.py',
                             creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(
            subprocess.Popen('python client.py -n test1',
                             creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(
            subprocess.Popen('python client.py -n test2',
                             creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(
            subprocess.Popen('python client.py -n test3',
                             creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ANSWER == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
