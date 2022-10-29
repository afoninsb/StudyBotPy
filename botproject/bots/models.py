from django.db import models


class BotAdmin(models.Model):
    chat = models.BigIntegerField('Telegram ID', unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    time = models.DateTimeField('Last login time', auto_now=True)
    pin = models.SlugField(max_length=50, blank=True)
    cur_bot = models.BigIntegerField(blank=True)

    def __str__(self):
        return (f'{self.first_name} {self.last_name}'
                f' | {self.chat}')


class Bot(models.Model):
    tg = models.CharField(
        'Telegram token',
        max_length=100,
        unique=True)
    login = models.CharField(
        'Telegram username',
        max_length=100,
        unique=True)
    name = models.CharField(
        'Bot name',
        max_length=100)
    type = models.IntegerField(default=1)
    password = models.CharField(
        max_length=50,
        default='pass123')
    active = models.BooleanField(default=False)
    lng = models.CharField(
        'Bot language',
        max_length=3,
        default='ru')
    admins = models.ManyToManyField(
        BotAdmin,
        related_name='bot')

    def __str__(self):
        return f'Бот "{self.name}": {self.login}'
