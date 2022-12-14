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
                url = f'/webhook/{cur_bot.tg}/'
                if settings.DEBUG:
                    data = {
                        'url': f'https://{settings.NGROK}{url}'
                    }
                else:
                    data = {
                        'url': f'{settings.BASE_URL}{url}'
                    }
                bot.set_webhook(data)
                bot.set_commands()
