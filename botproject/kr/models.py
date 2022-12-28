from bots.models import Bot
from django.db import models
from groups.models import Group, Spisok
from plans.models import PlanItem


class KR(models.Model):
    """Модель контрольной работы."""
    name = models.CharField('Название КР', max_length=100)
    kolzad = models.PositiveSmallIntegerField(
        'Кол-во заданий', default=1)
    item = models.OneToOneField(
        PlanItem, on_delete=models.CASCADE,
        related_name='kr',
        unique=True,
        verbose_name='Тема')
    bot = models.ForeignKey(
        Bot, on_delete=models.CASCADE,
        related_name='kr')

    def __str__(self):
        return self.name


class Task(models.Model):
    """Модель задания."""
    kr = models.ForeignKey(
        KR, on_delete=models.CASCADE,
        related_name='task')
    number = models.PositiveSmallIntegerField('Номер задания', default=1)
    text = models.TextField('Текст задачи', max_length=2000)
    img = models.ImageField('Изображение', upload_to='temp/', blank=True)

    def __str__(self):
        return self.text


class KROut(models.Model):
    """Лог выдачи контрольной работы."""
    kr = models.ForeignKey(
        KR, on_delete=models.CASCADE,
        related_name='kr_out')
    time = models.DateTimeField('Время раздачи', auto_now=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE,
        related_name='kr_out')
    deadline = models.DateTimeField('Дедлайн сдачи', null=True)

    class Meta:
        ordering = ['-time']


class TaskOut(models.Model):
    """Лог выдачи задания."""
    number = models.PositiveSmallIntegerField('Номер задания')
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE,
        related_name='task_out')
    krout = models.ForeignKey(
        KROut, on_delete=models.CASCADE,
        related_name='task_out')
    time = models.DateTimeField('Время раздачи', auto_now=True)
    user = models.ForeignKey(
        Spisok, on_delete=models.CASCADE,
        related_name='task_out')
