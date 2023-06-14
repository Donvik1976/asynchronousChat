"""
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий
сохранение данных в файле YAML-формата. Для этого:
a. Подготовить данные для записи в виде словаря, в котором первому ключу
соответствует список, второму — целое число, третьему — вложенный словарь, где
значение каждого ключа — это целое число с юникод-символом, отсутствующим в
кодировке ASCII (например, €);
b. Реализовать сохранение данных в файл формата YAML — например, в файл
file.yaml. При этом обеспечить стилизацию файла с помощью параметра
default_flow_style, а также установить возможность работы с юникодом:
 allow_unicode = True;
c. Реализовать считывание данных из созданного файла и проверить, совпадают ли
они с исходными.
"""

import yaml


data = {
    'items': ['computer', 'printer', 'keyboard', 'mouse'],
    'items_price': {
        'computer': '200\\u20ac-1000\\u20ac',
        'keyboard': '5\\u20ac-50\\u20ac',
        'mouse': '4\\u20ac-7\\u20ac',
        'printer': '100\\u20ac-300\\u20ac'
    },
    'items_quantity': 4
}

for key, value in data['items_price'].items():
    data['items_price'][key] = value.encode('utf-8').decode('unicode-escape')


with open('file.yaml', 'w', encoding='UTF-8') as file:
    yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


with open('file.yaml', 'r', encoding='UTF-8') as file:
    loaded_data = yaml.safe_load(file)


if data == loaded_data:
    print("Данные совпадают.")
else:
    print("Данные не совпадают.")
