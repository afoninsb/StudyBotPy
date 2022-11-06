from django.conf import settings

from edubot.main_classes import BotData, LocalData
from regbot.keyboards.inline import approve_admin
from regbot.models import Temp
from regbot.keyboards import hide_kbrd


def reg_start(message: dict, bot: BotData, local: LocalData) -> None:
    """Старт процедуры регистрации."""
    text = '''
    Добрый день!
    Вы беседуете с ботом платформы образовательных ботов StudyBot.Fun.
    Для отправки заявки надо пройти 5 простых шагов.

    Шаг 1. Введите Ваше имя (только Имя):'''
    answer = {
        'chat_id': local.chat_id,
        'text': text,
        'reply_markup': hide_kbrd()
    }
    local.user_edit(state='get_admin_first_name')
    bot.send_answer(answer)


def reg_first_name(message: dict, bot: BotData, local: LocalData) -> None:
    """Получили Имя и обрабатываем его.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        text = f'''
        Отлично, {message['text']}!

        Шаг 2. Введите вашу Фамилию (только Фамилию):'''
        local.user_edit(state='get_admin_last_name')
        local.temp_admin_edit(first_name=message['text'])
    else:
        text = 'Шаг 1. Введите Ваше имя (только Имя):'
    answer = {
        'chat_id': local.chat_id,
        'text': text,
        'reply_markup': hide_kbrd()
    }
    bot.send_answer(answer)


def reg_last_name(message: dict, bot: BotData, local: LocalData) -> None:
    """Получили Фамилию и обрабатываем её. Завершаем регистрацию.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        text = f'''
        Отлично, {local.user_first_name} {message['text']}!

        Шаг 3. Ведите организацию, в которой вы работаете:'''
        local.user_edit(state='get_admin_org')
        local.temp_admin_edit(last_name=message['text'])
    else:
        text = 'Шаг 2. Введите вашу Фамилию (только Фамилию):'
    answer = {
        'chat_id': local.chat_id,
        'text': text,
        'reply_markup': hide_kbrd()
    }
    bot.send_answer(answer)


def reg_org(message: dict, bot: BotData, local: LocalData) -> None:
    """Получили организацию и обрабатываем её. Завершаем регистрацию.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        text = '''Ещё немного :)

            Шаг 4. Введите вашу должность:'''
        local.user_edit(state='get_admin_position')
        local.temp_admin_edit(org=message['text'])
    else:
        text = 'Шаг 3. Ведите организацию, в которой вы работаете:'
    answer = {
        'chat_id': local.chat_id,
        'text': text,
        'reply_markup': hide_kbrd()
    }
    bot.send_answer(answer)


def reg_position(message: dict, bot: BotData, local: LocalData) -> None:
    """Получили позицию и обрабатываем её. Завершаем регистрацию.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        text = '''И последнее....

            Шаг 5. Объясните в 3-х предложениях, 
    зачем вам этот бот, 
    для чего будете его использовать:'''
        local.user_edit(state='get_admin_why')
        local.temp_admin_edit(position=message['text'])
    else:
        text = 'Шаг 4. Введите вашу должность:'
    answer = {
        'chat_id': local.chat_id,
        'text': text,
        'reply_markup': hide_kbrd()
    }
    bot.send_answer(answer)


def reg_why(message: dict, bot: BotData, local: LocalData) -> None:
    """Получили объяснение и обрабатываем его. Завершаем регистрацию.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if message.get('text'):
        text = '''Спасибо за информацию.
            Данные были отправлены супербоссу :)
            После его подтверждения, вы сможете работать на платформе.'''
        local.temp_admin_edit(why=message['text'])
        local.user_edit(state='')
        temp_admin = Temp.objects.get(chat=local.chat_id)
        text_to_boss = f'''Пришла заявка на нового админа.
            Имя: {temp_admin.first_name}
            Фамилия: {temp_admin.last_name}
            Организация: {temp_admin.org}
            Должность: {temp_admin.position}
            Пояснение: {temp_admin.why}'''
        answer_to_boss = {
            'chat_id': settings.BIG_BOSS_ID,
            'text': text_to_boss,
            'reply_markup': approve_admin(local.chat_id),
        }
        bot.send_answer(answer_to_boss)
    else:
        text = '''Объясните в 3-х предложениях, зачем вам этот бот, 
        для чего будете его использовать:'''
    answer = {
        'chat_id': local.chat_id,
        'text': text,
        'reply_markup': hide_kbrd()
    }
    bot.send_answer(answer)
