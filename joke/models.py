from django.db import models


class User(models.Model):
    address = models.CharField(
        null=False,
        max_length=30,
        blank=False
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.address


class Joke(models.Model):
    text = models.CharField(
        null=False,
        max_length=500,
        blank=False,
        unique=True
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = 'Шутка'
        verbose_name_plural = 'Шутки'

    def __str__(self):
        return self.text


class Log(models.Model):
    request_time = models.DateTimeField(
        null=False,
        blank=False
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    user_address = models.CharField(
        null=False,
        max_length=30,
        blank=False
    )

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

    def __str__(self):
        return self.request_time.strftime('%b %d %Y %H:%M:%S')
