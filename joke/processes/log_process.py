from django.utils import timezone

from joke.models import User
from joke.repository import LogRepository


class Logging:
    """
    Данный класс отвечает за логирование запросов внутри приложения
    """

    @staticmethod
    def log_info(user: User):
        time_now = timezone.localtime(timezone.now())
        LogRepository.create(
            user_id=user.id,
            user_address=user.address,
            time=time_now
        )
