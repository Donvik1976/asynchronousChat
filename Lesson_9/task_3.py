"""
Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
(использовать модуль tabulate). Таблица должна состоять из двух колонок
"""
from tabulate import tabulate
from task_1 import host_ping


def host_range_ping_tab(start_ip, end_ip):
    start_ip_octet = start_ip.split('.')
    end_ip_octet = end_ip.split('.')
    host = []
    for i in range(int(start_ip_octet[3]), int(end_ip_octet[3]) + 1):
        ip = f"{'.'.join(start_ip_octet[0:3])}.{i}"
        host.append(ip)

    results = host_ping(host)
    table_headers = ['IP-адрес', 'Статус']
    table = tabulate(results, headers=table_headers, tablefmt='grid')
    print(table)


if __name__ == '__main__':
    host_range_ping_tab('216.58.210.182', '216.58.210.193')

