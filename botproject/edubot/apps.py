from django.apps import AppConfig
from django.conf import settings


class EdubotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'edubot'

    def ready(self):
        from bots.models import Bot

        from .main_classes import BotData

        if bots := Bot.objects.all():
            for cur_bot in bots:
                bot = BotData(cur_bot.tg)
                data = {
                    'url': f'{settings.BASE_URL}/webhook/{cur_bot.tg}/'
                    # 'url': f'https://76d7-95-72-27-229.eu.ngrok.io/webhook/{cur_bot.tg}/'
                }
                bot.set_webhook(data)
                bot.set_commands()
