import unittest

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, PRESENCE, TIME, USER, ERROR
from server import process_client_message


class TestServer(unittest.TestCase):
    dict_error = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    dict_ok = {RESPONSE: 200}
    """
    Проверяем функцию: if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
    and USER in message and message[USER][ACCOUNT_NAME] == 'Guest'
    Начальные данные:
    {'action': 'presence', 'time': 17.44, 'user': {'account_name': 'Guest'}}
    """

    def test_no_action(self):
        """Если нет действия"""
        self.assertEqual(process_client_message(
            {TIME: '17.44', USER: {ACCOUNT_NAME: 'Guest'}}), self.dict_error
        )

    def test_unknown_action(self):
        """Неизвестное действие"""
        self.assertEqual(process_client_message(
            {ACTION: 'wrong', TIME: '17.44', USER: {ACCOUNT_NAME: 'Guest'}}), self.dict_error
        )

    def test_no_time(self):
        """Нет параметра time"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.dict_error
        )

    def test_no_user(self):
        """Нет параметра user"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '17.44'}), self.dict_error
        )

    def test_unknown_user(self):
        """Неизвестный пользователь"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '17.44', USER: {ACCOUNT_NAME: 'Victor'}}), self.dict_error
        )

    def test_сorrect_request(self):
        """Корректный запрос"""
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '17.44', USER: {ACCOUNT_NAME: 'Guest'}}), self.dict_ok
        )


if __name__ == '__main__':
    unittest.main()
