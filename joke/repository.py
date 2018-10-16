from datetime import datetime
from typing import List

from .models import Joke
from .models import Log
from .models import User


class JokeNotExistException(Exception):
    """
    Искомый объект не найден в таблице Jokes
    """


class UserRepository:
    """
    Работа с сущностью User
    """

    @staticmethod
    def get_user_by_address(address: str) -> User or None:
        """
        Проверка на существование пользователя
        :param address: ip адрес клиента
        :return: объект пользователя или None, если он не существует
        """
        try:
            user = User.objects.get(address=address)
            return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def create_new(address: str) -> User:
        """
        Создание нового пользователя в системе
        :param address: ip адрес клиента
        :return: объект нового пользователя
        """
        new_user = User.objects.create(address=address)
        return new_user


class JokeRepository:
    """
    Работа с сущностью Joke
    """

    @staticmethod
    def get_all_user_jokes(user_id: int) -> List[Joke]:
        """
        Получение всех объектов Joke текущего пользователя
        :param user_id: id пользователя
        :return: Список всех объектов базы данных
        """
        jokes = Joke.objects.filter(user_id=user_id).order_by('id')
        return jokes

    @staticmethod
    def update_text(id: int,
                    new_text: str):
        """
        Обновление существующей записи
        :param id: id записи
        :param new_text: новый текст шутки
        """
        Joke.objects.filter(id=id) \
            .update(text=new_text)

    @staticmethod
    def delete(id: int):
        """
        Удаление существующей записи
        :param id: id записи
        """
        Joke.objects.filter(id=id) \
            .delete()

    @staticmethod
    def get_all_jokes() -> List[str]:
        """
        Получение текта всех шуток из базы
        :return: Список текстов
        """
        return Joke.objects.values_list('text', flat=True)

    @staticmethod
    def create(text: str,
               user_id: int):
        """
        Создание новой записи в таблице Joke
        :param text: текст шутки
        :param user_id: id пользователя, сгенерировшего шутку
        """
        Joke.objects.create(
            text=text,
            user_id=user_id
        )

    @staticmethod
    def get_by_id(id: int) -> Joke:
        """
        Получение записи из таблицы по идетификатору
        :param id: id записи
        """
        try:
            return Joke.objects.get(id=id)
        except Joke.DoesNotExist:
            raise JokeNotExistException


class LogRepository:
    """Работа с сущностью Log"""

    @staticmethod
    def create(user_id: int, user_address: str, time: datetime):
        Log.objects.create(
            user_id=user_id,
            user_address=user_address,
            request_time=time
        )
