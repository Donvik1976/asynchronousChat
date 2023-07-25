import time
import unittest

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, PRESENCE, TIME, USER, ERROR
from client import create_presence, process_ans


class TestClient(unittest.TestCase):
    """
    Проверим функцию create_presence
    Так, как TIME у нас переменная, и зависит от конкретного времени запуска
    в словарь для сравнения я вставил функцию time(), иначе выдает ошибку
    """

    def test_create_presence(self):
        self.assertEqual(
            create_presence(),
            {ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: 'Guest'}}
        )

    """
    Теперь проверим функцию process_ans
    """

    def test_process_ans_400(self):
        """Выдает ответ 400"""
        self.assertEqual(process_ans(
            {RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request'
        )

    def test_process_ans_200(self):
        """Выдает ответ 200"""
        self.assertEqual(process_ans(
            {RESPONSE: 200}), '200 : OK'
        )

    def test_process_no_response(self):
        """
        Если поля response нет в ответе
        должна появиться ValueError
        'process_ans' передается как объект функции, а не вызывается непосредственно
        """
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
