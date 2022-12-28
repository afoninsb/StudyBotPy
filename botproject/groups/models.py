from django.db import models

from bots.models import Bot
from plans.models import Plan


class Spisok (models.Model):
    """Модель учащегося."""
    chat = models.BigIntegerField(
        'Telegram ID',
        unique=True)
    first_name = models.CharField(
        'Имя',
        max_length=20)
    last_name = models.CharField(
        'Фамилия',
        max_length=20)
    bots = models.ManyToManyField(
        Bot,
        related_name='spisok')
    state = models.CharField(
        max_length=20,
        blank=True, null=True,)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        ordering = ['last_name']


class Group(models.Model):
    """Модель группы."""
    name = models.CharField(
        'Название группы',
        max_length=100)
    pin = models.CharField(
        'Пин-код',
        max_length=8,
        unique=True)
    bot = models.ForeignKey(
        Bot, on_delete=models.CASCADE,
        related_name='groupbot')
    users = models.ManyToManyField(
        Spisok,
        related_name='groupuser')
    plans = models.ManyToManyField(
        Plan,
        related_name='groupplan')

    def __str__(self):
        return f'{self.name}'
