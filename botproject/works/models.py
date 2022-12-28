from bots.models import Bot
from django.db import models
from groups.models import Group, Spisok
from kr.models import KROut
from plans.models import PlanItem


class Work(models.Model):
    """Модель работы ученика."""
    # Типы работ ученика
    TYPES = (
        ('k', 'Контрольная работа'),
        ('p', 'Практическая работа'),
    )
    STATUS = (
        ('passed', 'Работа сдана'),
        ('done', 'Работа зачтена'),
        ('rejected', 'Работа отклонена'),
    )
    user = models.ForeignKey(
        Spisok, on_delete=models.CASCADE,
        related_name='work')
    item = models.ForeignKey(
        PlanItem, on_delete=models.CASCADE,
        related_name='work')
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE,
        related_name='work')
    bot = models.ForeignKey(
        Bot, on_delete=models.CASCADE,
        related_name='work')
    type = models.CharField(max_length=1, choices=TYPES)
    time = models.DateTimeField(auto_now=True)
    krout = models.ForeignKey(
        KROut, on_delete=models.CASCADE,
        related_name='work',
        blank=True, null=True)
    link = models.URLField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='passed')
    review = models.TextField(
        max_length=1000,
        blank=True)
    mark = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-time']
