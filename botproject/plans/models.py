from django.db import models

from bots.models import Bot


class Plan(models.Model):
    """Модель тематического плана."""
    name = models.CharField(
        'Название плана',
        max_length=33,
        help_text='Максимальная длина 33 символа (ограничение Telegram)'
    )
    bot = models.ForeignKey(
        Bot, on_delete=models.CASCADE,
        related_name='plan',
    )

    def __str__(self):
        return f'{self.name}'


class PlanItem(models.Model):
    """Модель темы в тематическом плане."""
    # Типы тем
    TYPES = (
        ('t', 'Теоретический материал'),
        ('k', 'Контрольная работа'),
        ('p', 'Практическая работа'),
    )
    name = models.CharField(
        'Название темы',
        max_length=33,
        help_text='Максимальная длина 33 символа (ограничение Telegram)'
    )
    link = models.URLField('Ссылка на материалы', blank=True)
    type = models.CharField('Тип занятия', max_length=1, choices=TYPES)
    weight = models.PositiveSmallIntegerField(default=0)
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE,
        related_name='plan_item')

    def __str__(self):
        return f'{self.name}'
