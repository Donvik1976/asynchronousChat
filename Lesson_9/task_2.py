"""
2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""
from task_1 import host_ping


def host_range_ping(start_ip, end_ip):
    start_ip_octet = start_ip.split('.')
    end_ip_octet = end_ip.split('.')
    host = []
    for i in range(int(start_ip_octet[3]), int(end_ip_octet[3]) + 1):
        ip = f"{'.'.join(start_ip_octet[0:3])}.{i}"
        host.append(ip)
    return host_ping(host)


if __name__ == '__main__':
    addresses = host_range_ping('216.58.210.182', '216.58.210.193')
    for i in addresses:
        print(f'Узел {i[0]} {i[1]}')
