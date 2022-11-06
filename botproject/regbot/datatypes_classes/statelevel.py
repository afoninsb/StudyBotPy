"""
    Класс направления Состояние юзера.
    Идет перенаправление в зависимости от полученного состояния юзера.
"""

from .datatypesclass import Observer, Subject
from .states import exchange_message, registration


class StateDistributor(Observer):
    def update(self, subject: Subject, bot, local, **kwargs) -> None:
        pathes = {
            'start': registration.reg_start,
            'get_admin_first_name': registration.reg_first_name,
            'get_admin_last_name': registration.reg_last_name,
            'get_admin_org': registration.reg_org,
            'get_admin_position': registration.reg_position,
            'get_admin_why': registration.reg_why,
            'message_to_admins': exchange_message.message_to_admins,
            'support': exchange_message.support,
            'reply': exchange_message.reply,
        }
        state = subject._state.split(':')[0]
        if state in pathes:
            pathes[state](kwargs['message'], bot, local)
