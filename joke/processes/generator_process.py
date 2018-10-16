import re

import requests

from anekdot import settings
from joke.repository import JokeRepository


class GeekJokeSideError:
    """
    Ошибка, возникающая при невозможности подключиться к api geek.jokes
    """


class NoUniqueJokeError:
    """
    Ошибка, возникающая при исчерпывании лимита получения уникальных записей от api
    """


class Generator:
    """
    Данный класс содержит в себе логику работы с api geek.jokes
    """

    @staticmethod
    def get_new_joke() -> str:
        """
        Генерация новой шутки
        :return: текст шутки
        """
        safe_index = 0
        all_jokes = JokeRepository.get_all_jokes()
        new_joke = Generator.__take_new_joke()
        while new_joke in all_jokes:
            new_joke = Generator.__take_new_joke()
            if safe_index == 5:
                raise NoUniqueJokeError
            safe_index += 1

        return new_joke

    @staticmethod
    def __take_new_joke() -> str:
        """
        Получение ответа от сервиса и его обработка
        :return: текст шутки
        """
        with requests.Session() as session:
            response = session.get(settings.JOKE_URL)
            if response.status_code == 200:
                joke = Generator.__clean_joke(response.text)
                return joke
            else:
                raise GeekJokeSideError

    @staticmethod
    def __clean_joke(text: str) -> str:
        """
        Удаление всех спец. символов из текста шутки
        :param text: текст из запроса
        :return: очищенный текст
        """
        reg = re.compile('[^a-zA-Z,.!? ]')
        return reg.sub('', text)
