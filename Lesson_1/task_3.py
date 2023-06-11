"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" исключение,
придумайте как это сделать
"""

words = ['attribute', 'класс', 'функция', 'type']
unconvertible_words = set()

for word in words:
    try:
        _ = bytes(word, 'ascii')
    except UnicodeEncodeError:
        unconvertible_words.add(word)

print(f"Невозможно записать в байтовом типе следующие слова: "
      f"{', '.join(unconvertible_words)}")
