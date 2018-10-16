import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from joke.processes.log_process import Logging
from .processes.generator_process import GeekJokeSideError
from .processes.generator_process import Generator
from .processes.generator_process import NoUniqueJokeError
from .processes.joke_process import JokeNotExistError
from .processes.joke_process import JokeProcess
from .processes.joke_process import NoPermissionToDeleteError
from .processes.joke_process import NoPermissionToUpdateError
from .repository import JokeRepository
from .serializers import JokeListSerializer
from .serializers import JokeTextSerializer


class JokeListAPIView(APIView):
    """
    Данный класс обрабаотывает запросы приходящие по адрессу:
    /jokes
    """


    def get(self, request):
        """
        Данный метод возвращает текущему пользователю все его шутки в json формате
        """
        user = request.api_user
        Logging.log_info(user)
        user_jokes = JokeProcess.get_all_user_jokes(user_id=user.id)
        serializer = JokeListSerializer(data=user_jokes)
        if not serializer.is_valid():
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK,
                        data=serializer.validated_data,
                        content_type='application/json')


class JokeAPIView(APIView):
    """
    Данный эндпоинт обрабатывает все запросы на редактирвоание сущности шуток
    /jokes/1
    """

    def put(self, request, pk):
        """
        Обновление существующих записей в базе данных
        :param pk: id записи в базе данных
        """
        user = request.api_user
        Logging.log_info(user)
        serializer = JokeTextSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=json.dumps({
                                'error_message': 'Send json is not valid'}),
                            content_type='application/json')
        joke_text = serializer.validated_data['text']
        try:
            JokeProcess.update_joke(user_id=user.id,
                                    joke_id=pk,
                                    new_text=joke_text)
        except JokeNotExistError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=json.dumps({
                                'error_message': 'Item not exist'}),
                            content_type='application/json')
        except NoPermissionToUpdateError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=json.dumps({
                                'error_message': 'Have no permission to update'}),
                            content_type='application/json')
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Удаление существующей записи в базе данных
        :param pk: id записи в базе данных
        """
        user = request.api_user
        Logging.log_info(user)
        try:
            JokeProcess.delete_joke(user_id=user.id, joke_id=pk)
        except JokeNotExistError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=json.dumps({
                                'error_message': 'Item not exist'}),
                            content_type='application/json')
        except NoPermissionToDeleteError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=json.dumps({
                                'error_message': 'Have no permission to delete'}),
                            content_type='application/json')
        return Response(status=status.HTTP_200_OK)


class GenerateJokeAPIView(APIView):
    """
    Данный эндпоинт генерирует пользователю новые данные
    """

    def get(self, request):
        """
        Генерация новой уникальной шутки через стороннее api
        """
        user = request.api_user
        Logging.log_info(user)
        try:
            joke = Generator.get_new_joke()
        except GeekJokeSideError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=json.dumps({
                                'error_message': 'geek-jokes.sameerkumar error side'}),
                            content_type='application/json')
        except NoUniqueJokeError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=json.dumps({
                                'error_message': 'There is no unique jokes anymore'}),
                            content_type='application/json')
        JokeRepository.create(joke, user.id)
        serializer = JokeTextSerializer(data={'text': joke})
        if not serializer.is_valid():
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK,
                        data=serializer.validated_data,
                        content_type='application/json')
