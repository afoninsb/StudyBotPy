import json

from bots.models import BotAdmin


def main_kbrd(chat_id: int) -> str:
    """Главная клавиатура бота.
    Args:
        chat_id (int): Telegram chat_id юзера.
    Returns:
        str: Клавиатура в формате json.
    """
    keyboard = [
        [
            {'text': 'План'},
            {'text': 'Сообщение учителю'},
        ]
    ]
    if BotAdmin.objects.filter(chat=chat_id):
        buttons_admin = [
            {'text': 'Администрировать'},
        ]
        keyboard.append(buttons_admin)
    mkbrd = {
        'keyboard': keyboard,
        'one_time_keyboard': True,
        'resize_keyboard': True,
    }
    return json.dumps(mkbrd)
