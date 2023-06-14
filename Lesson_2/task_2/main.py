"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с
информацией о заказах. Написать скрипт, автоматизирующий его заполнение
данными. Для этого:
a. Создать функцию write_order_to_json(), в которую передается 5 параметров:
товар(item), количество (quantity), цена (price), покупатель (buyer), дата
(date). Функция должна предусматривать запись данных в виде словаря в файл
orders.json. При записи данных указать величину отступа в 4 пробельных символа;
b. Проверить работу программы через вызов функции write_order_to_json() с
передачей в нее значений каждого параметра.
"""
import json


def write_order_to_json(item, quantity, price, buyer, date):
    order = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }
    with open('orders.json', 'r+', encoding='UTF-8') as file:
        content = json.load(file)
        content['orders'].append(order)
        file.seek(0)
        json.dump(content, file, indent=4, ensure_ascii=False)



write_order_to_json('принтер', 10, 6700, 'Ivanov', '05.03.2021')
write_order_to_json('scaner', 20, 10000, 'Петров', '22.08.2022')
write_order_to_json('копир', 12, 8200, 'Sidorov', '12.06.2023')
