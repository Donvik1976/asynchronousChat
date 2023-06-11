import chardet

with open('test_file.txt', 'w', encoding='utf-16') as file:
    file.write('сетевое программирование\n')
    file.write('сокет\n')
    file.write('декоратор\n')

with open('test_file.txt', 'rb') as file:
    content = file.read()
    default_encoding = chardet.detect(content)['encoding']

content_text = content.decode(default_encoding)
with open('test_file.txt', 'w', encoding='utf-8', newline='') as file:
    file.write(content_text)

print(f'Кодировка файла по умолчанию: {default_encoding}')

# Принудительное открытие файла в формате Unicode и вывод содержимого
with open('test_file.txt', 'r', encoding='utf-8') as file:
    unicode_content = file.read()

print('Содержимое файла в формате Unicode:')
print(unicode_content)
