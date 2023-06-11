"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""
import subprocess
import chardet

websites = ["yandex.ru", "youtube.com"]

for website in websites:
    ping_process = subprocess.Popen(["ping", website], stdout=subprocess.PIPE)
    output, _ = ping_process.communicate()
    """
    Метод communicate() запускает процесс пинга и возвращает кортеж, 
    содержащий вывод процесса и код завершения. Здесь мы присваиваем только 
    вывод процесса переменной output, а символ _ используется для игнорирования
    кода завершения.
    """
    result_encoding = chardet.detect(output)["encoding"]
    decoded_output = output.decode(result_encoding)
    print(f"Результат пинга для {website}:")
    print(decoded_output)
