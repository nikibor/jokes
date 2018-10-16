from typing import Dict
from typing import List

from joke.repository import JokeNotExistException
from joke.repository import JokeRepository


class JokeNotExistError(Exception):
    """
    Искомая запись не найдена в базе данных
    """


class NoPermissionToUpdateError(Exception):
    """
    Нет прав на редактирование записи
    """


class NoPermissionToDeleteError(Exception):
    """
    Нет прав на удаление записи
    """


class JokeProcess:
    """
    Процессы взаимдействия с сущностью Joke
    """

    @staticmethod
    def get_all_user_jokes(user_id: int) -> Dict[str, List]:
        """
        Получение всех текстов и id шуток пользователя
        :param user_id: id пользователя
        :return: список шуток
        """
        jokes = JokeRepository.get_all_user_jokes(user_id=user_id)
        joke_texts = []
        for joke in jokes:
            joke_texts.append(
                {
                    'id': joke.id,
                    'text': joke.text
                })

        return {
            'jokes': joke_texts
        }

    @staticmethod
    def update_joke(user_id: int, joke_id: int, new_text):
        """
        Обновление шутки
        :param user_id: id пользователя
        :param joke_id: id шутки
        :param new_text: новый текст шутки
        """
        try:
            joke = JokeRepository.get_by_id(id=joke_id)
        except JokeNotExistException:
            raise JokeNotExistError

        user_jokes = JokeRepository.get_all_user_jokes(user_id=user_id)
        if joke not in user_jokes:
            raise NoPermissionToUpdateError
        JokeRepository.update_text(id=joke_id, new_text=new_text)

    @staticmethod
    def delete_joke(user_id: int, joke_id):
        """
        Удаление шутки
        :param user_id: id пользователя
        :param joke_id: id шутки
        """
        try:
            joke = JokeRepository.get_by_id(id=joke_id)
        except JokeNotExistException:
            raise JokeNotExistError

        user_jokes = JokeRepository.get_all_user_jokes(user_id=user_id)
        if joke not in user_jokes:
            raise NoPermissionToDeleteError
        JokeRepository.delete(joke_id)
