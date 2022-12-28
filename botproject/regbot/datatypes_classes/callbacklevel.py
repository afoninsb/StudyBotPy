"""
    Класс направления Сallback_query.
    Идет перенаправление в зависимости от полученного содержимого
    ответа callback_query.
"""

from django.conf import settings

from bots.models import BotAdmin
from groups.models import Spisok
from regbot.keyboards.main import hide_kbrd, main_kbrd
from regbot.models import Temp

from .datatypesclass import Observer, Subject


class CallbackApprove(Observer):
    def update(self, subject: Subject, bot, local, **kwargs) -> None:
        if subject._state == 'approve':
            data = kwargs['callback_query'].split(':')
            temp_user = Temp.objects.get(chat=data[1])
            try:
                BotAdmin.objects.create(
                    chat=data[1],
                    first_name=temp_user.first_name,
                    last_name=temp_user.last_name,
                    cur_bot=1
                )
            except Exception as exc:
                print(exc)
            Spisok.objects.filter(chat=data[1]).update(
                first_name=temp_user.first_name,
                last_name=temp_user.last_name,
            )
            Temp.objects.filter(chat=data[1]).delete()
            text = '''Ваша заявка одобрена.

                На клавиатуре нажмите кнопу "Администрировать",
                чтобы пройти в административную панель.'''
            answer = {
                'chat_id': data[1],
                'text': text,
                'reply_markup': main_kbrd(data[1]),
            }
            bot.send_answer(answer)
            answer_to_boss = {
                'chat_id': settings.BIG_BOSS_ID,
                'text': 'Отправлено одобрение',
            }
            bot.send_answer(answer_to_boss)


class CallbackReject(Observer):
    def update(self, subject: Subject, bot, local, **kwargs) -> None:
        if subject._state == 'reject':
            data = kwargs['callback_query'].split(':')
            Temp.objects.filter(chat=data[1]).delete()
            Spisok.objects.filter(chat=data[1]).delete()
            answer = {
                'chat_id': data[1],
                'text': 'Ваша заявка отклонена!',
                'reply_markup': hide_kbrd(),
            }
            bot.send_answer(answer)
            answer_to_boss = {
                'chat_id': settings.BIG_BOSS_ID,
                'text': 'Отправлен отказ',
            }
            bot.send_answer(answer_to_boss)


class CallbackReply(Observer):
    def update(self, subject: Subject, bot, local, **kwargs) -> None:
        if subject._state == 'reply':
            data = kwargs['callback_query'].split(':')
            local.user_edit(state=f'reply:{data[1]}')
            send_user = Spisok.objects.get(chat=data[1])
            answer = {
                'chat_id': local.chat_id,
                'text':
                (f'Отправьте ваш ответ (только текст). Его получит '
                 f'{send_user.first_name} {send_user.last_name}'),
            }
            bot.send_answer(answer)
