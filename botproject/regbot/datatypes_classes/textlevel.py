"""
    Класс направления Текст.
    Идет перенаправление в зависимости от полученного текста.
"""

from uuid import uuid1

from bots.models import Bot, BotAdmin
from regbot.keyboards import admin_kbrd, main_kbrd, hide_kbrd
from edubot.main_classes import BotData, LocalData

from .datatypesclass import Observer, Subject


class TextMessageToAdmins(Observer):
    def update(self, subject: Subject, bot: BotData, local: LocalData) -> None:
        if subject._state == 'Сообщение админам':
            local.user_edit(state='message_to_admins')
            answer = {
                'chat_id': local.chat_id,
                'text': 'Пишите (только текст):',
            }
            bot.send_answer(answer)


class TextSupport(Observer):
    def update(self, subject: Subject, bot: BotData, local: LocalData) -> None:
        if subject._state == 'Техподдержка':
            local.user_edit(state='support')
            answer = {
                'chat_id': local.chat_id,
                'text': '''Сообщите, о каком боте идет речь и суть проблемы.
                Пишите сообщение в техподдержку (только текст):''',
            }
            bot.send_answer(answer)


class TextGoToPanel(Observer):
    def update(self, subject: Subject, bot: BotData, local: LocalData) -> None:
        if subject._state == 'Администрировать':
            pin = str(uuid1())
            BotAdmin.objects.filter(chat=local.chat_id).update(pin=pin)
            answer = {
                'chat_id': local.chat_id,
                'text': 'Для входа в админпанель нажмите кнопку:',
                'reply_markup': admin_kbrd(local.chat_id, pin),
            }
            bot.send_answer(answer)


class TextHaHaHa(Observer):
    def update(self, subject: Subject, bot: BotData, local: LocalData) -> None:
        if subject._state not in ['Администрировать',
                'Сообщение админам', 'Техподдержка']:
            answer = {
                'chat_id': local.chat_id,
                'text': 'Ага... и вам приветик!',
            }
            if local.is_admin:
                answer['reply_markup'] = main_kbrd(local.chat_id)
            else:
                answer['reply_markup'] = hide_kbrd()
            bot.send_answer(answer)
