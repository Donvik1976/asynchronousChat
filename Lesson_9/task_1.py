"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping
будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел
должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять
их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес
сетевого узла должен создаваться с помощью функции ip_address().
"""
import platform
import subprocess
import ipaddress
import socket


def host_ping(hosts):
    results = []
    for host in hosts:
        ip_sock = socket.gethostbyname(host)
        ip = ipaddress.ip_address(ip_sock)

        parameter = '-n' if platform.system().lower() == 'windows' else '-c'
        command = f'ping {parameter} 1 {ip}'
        result = subprocess.run(command, shell=True, capture_output=True)

        if result.returncode == 0:
            status = 'доступен'
        else:
            status = 'недоступен'

        results.append([host, status])
    return results


if __name__ == '__main__':
    websites = ['google.com', '192.168.0.1', '216.58.210.192', 'yandex.ru',
                'youtube.com']
    for i in host_ping(websites):
        print(f'Узел {i[0]} {i[1]}')
