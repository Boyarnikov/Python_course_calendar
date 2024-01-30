import os
import json

import unittest
from User import User
from Backend import Backend


class TestUserEvent(unittest.TestCase):
    def setUp(self):
        self.user = User()
        self.user.create_user(name='Павел', pwd='1234')

    def test_createUser(self):
        '''тестируем @имя и создание пароля-hash'''

        self.assertEqual(self.user.get_name(), '@Павел')
        self.assertEqual(self.user.get_hash_pwd(), '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4')

    def test_addUser(self):
        '''Проверяем что пользователь добавился в domain.csv'''

        Backend.add_user_bk(self.user.get_name(), self.user.get_hash_pwd())

        self.assertTrue(Backend.check_user_domain(self.user.get_name()))

    def test_usercsv(self):
        '''Проверяем создание в date_base/ одноименного файла для хранения мероприятий'''

        self.assertTrue('@Павел.csv' in os.listdir('./data_base'))

    def test_add_delEvent(self):
        '''проверяем что в файл с мероприятиями записалось событие, время хранится в unix секундах'''

        _name = self.user.get_name()
        old_len_csv = len(Backend.events_from_csv(_name))
        data_set = {'date': 1706648400, 'name': 'ДР', 'description': 'День рождение Лизы, не забыть цветы!'}
        Backend.write_event(json_data=json.dumps({_name: data_set}))
        'проверяем что длина csv увеличилась'
        self.assertEqual(len(Backend.events_from_csv(_name)), old_len_csv+1)

        Backend.del_event_csv(_name, data_set['date'])
        'проверяем что запись удалилась'
        self.assertEqual(len(Backend.events_from_csv(_name)), old_len_csv)

    def tearDown(self):
        del self.user


if __name__ == '__main__':
    unittest.main()
