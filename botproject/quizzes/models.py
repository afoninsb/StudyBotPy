from django.db import models
from plans.models import Plan
from bots.models import Bot

TYPES = (
    ('1', 'Один правильный'),
    ('2', 'Несколько правильных'),
    ('3', 'Текстовый ответ'),
    ('4', 'Упорядочить'),
)


class Quiz(models.Model):
    name = models.CharField(
        'Название вопроса',
        max_length=255,
        help_text='Назовите вопрос (для себя)'
    )
    type = models.CharField(
        'Тип вопроса',
        max_length=1,
        choices=TYPES,
        help_text='Укажите тип вопроса'
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE,
        related_name='quiz',
        help_text='Укажите тематический план, к которому относится вопрос'
    )
    text = models.TextField(
        'Текст вопроса',
        max_length=2000,
        help_text='Введите текст вопроса'
    )
    img = models.ImageField(
        'Изображение',
        upload_to='temp/',
        blank=True,
        help_text='Загрузите изображение (.jpg, .png)'
    )
    right = models.CharField(
        'Правильный ответ',
        max_length=255,
    )
    bot = models.ForeignKey(
        Bot, on_delete=models.CASCADE,
        related_name='quiz',
    )

    def __str__(self):
        return f'{self.name}'


class Answer(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE,
        related_name='answer',
    )
    text = models.TextField(
        'Текст ответа',
        max_length=2000,
        help_text='Введите текст ответа'
    )

    def __str__(self):
        return f'{self.text}'[:50]
