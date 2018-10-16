from django.utils.deprecation import MiddlewareMixin

from joke.repository import UserRepository


class ClientMiddleware(MiddlewareMixin):
    """
    Проверка клиентских запросов и автоматическая авторизация пользователей
    """

    def process_request(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        user = UserRepository.get_user_by_address(address=ip)
        if user:
            request.api_user = user
        else:
            request.api_user = UserRepository.create_new(address=ip)
