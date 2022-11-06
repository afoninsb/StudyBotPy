"""
    Класс направления Команда.
    Идет перенаправление в зависимости от полученной комманды бота.
"""

from .datatypesclass import Observer, Subject


class CommandCancel(Observer):
    def update(self, subject: Subject, bot, local) -> None:
        if subject._state == 'cancel':
            local.user_edit(state='')
            answer = {
                'chat_id': local.chat_id,
                'text': 'Текущая операция отменена!',
            }
            bot.send_answer(answer)
