"""
A. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список.
Должно получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список для
хранения данных отчета — например, main_data — и поместить в него названия
столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код
продукта», «Тип системы». Значения для этих столбцов также оформить в виде
списка и поместить в файл  main_data (также для каждого файла);
B. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;
C. Проверить работу программы через вызов функции write_to_csv().

Изготовитель системы, Название ОС, Код продукта, Тип системы
"""
import csv
import glob
import re

file_pattern = 'info_*'
files = glob.glob(file_pattern)


def get_data(count_files):
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта',
                  'Тип системы']]
    for i in range(1, count_files + 1):
        with open(f'info_{i}.txt', 'r') as file:
            content = file.read()
            os_prod_reg = re.compile(r'Изготовитель системы:\s*\S*')
            os_prod_list.append(os_prod_reg.findall(content)[0].split()[2])
            os_name_reg = re.compile(r'Название ОС:\s*.*(?=\n)')
            os_name_list.append(
                ' '.join(os_name_reg.findall(content)[0].split()[3:5]))
            os_code_reg = re.compile(r'Код продукта:\s*\S*')
            os_code_list.append(os_code_reg.findall(content)[0].split()[2])
            os_type_reg = re.compile(r'Тип системы:\s*\S*')
            os_type_list.append(os_type_reg.findall(content)[0].split()[2])

            main_data.append(
                [i, os_prod_list[-1], os_name_list[-1], os_code_list[-1],
                 os_type_list[-1]])

    return os_prod_list, os_name_list, os_code_list, os_type_list, main_data


def write_to_csv(csv_file):
    os_prod_list, os_name_list, os_code_list, os_type_list, \
        main_data = get_data(len(files))

    with open(csv_file, 'w', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(main_data)

    print(f"Данные успешно сохранены в файл: {csv_file}")


write_to_csv('data-report.csv')
