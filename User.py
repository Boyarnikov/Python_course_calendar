"""
Пользователь - имеет логин и пароль, а так же календарь.
у пользователя есть итендифекатор начинающийся с @
"""
import hashlib  # hashlib.sha256(pwd.encode()).hexdigest()


class User:
    _name = ''
    _pwd = None

    def create_user(self, name, pwd):
        self._name = '@' + name
        self._pwd = hashlib.sha256(pwd.encode()).hexdigest()

    def get_name(self):
        return self._name

    def get_hash_pwd(self):
        return self._pwd
