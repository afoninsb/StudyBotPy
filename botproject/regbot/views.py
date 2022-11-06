import json
from uuid import uuid1

from bots.models import BotAdmin
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from edubot.main_classes import BotData, LocalData
from groups.models import Spisok

from .models import Temp


def hide_kbrd() -> json:
    """Скрываем клавиатуру"""
    return json.dumps({'hide_keyboard': True})


def approve_admin(chat_id: int) -> json:
    """Клавиатура Одобрить/Отклонить для заявки в даины.
    Args:
        chat_id (int): Telegram chat_id юзера.
    Returns:
        json: Клавиатура в формате json.
    """
    akbd = {}
    keyboard = []
    inline_button = [
        {
            'text': 'Одобрить',
            'callback_data': f'approve:{chat_id}'
        },
        {
            'text': 'Отклонить',
            'callback_data': f'reject:{chat_id}'
        }
    ]
    keyboard.append(inline_button)
    akbd['inline_keyboard'] = keyboard
    return json.dumps(akbd)


def main_kbrd(chat_id: int) -> json:
    """Главная клавиатура бота.
    Args:
        chat_id (int): Telegram chat_id юзера.
    Returns:
        json: Клавиатура в формате json.
    """
    mkbrd = {}
    keyboard = [
        [
            {'text': 'Администрировать'},
        ]
    ]
    if int(chat_id) == int(settings.BIG_BOSS_ID):
        bbbutton = [{'text': 'Сообщение админам'}]
    else:
        bbbutton = [{'text': 'Техподдержка'}]
    keyboard.append(bbbutton)
    mkbrd['keyboard'] = keyboard
    mkbrd['one_time_keyboard'] = False
    mkbrd['resize_keyboard'] = True
    return json.dumps(mkbrd)


def admin_kbrd(chat_id: int, pin: str) -> json:
    """Кнопка Войти в административную панель.
    Args:
        chat_id (int): Telegram chat_id юзера.
        pin (str): pin-код для входа в админпанель.
    Returns:
        json: Клавиатура в формате json.
    """
    akbd = {}
    keyboard = []
    inline_button = [{
        'text': 'Войти в административную панель',
        'url': f"{settings.BASE_URL}/enter/{chat_id}/{pin}/"
    }]
    keyboard.append(inline_button)
    akbd['inline_keyboard'] = keyboard
    return json.dumps(akbd)


def reply_kbrd(chat_id: int) -> json:
    """Кнопка Ответить при переписке.
    Args:
        chat_id (int): Telegram chat_id юзера.
    Returns:
        json: Клавиатура в формате json.
    """
    rkbd = {}
    keyboard = []
    inline_button = [{
        'text': 'Ответить',
        'callback_data': f'reply:{chat_id}'
    }]
    keyboard.append(inline_button)
    rkbd['inline_keyboard'] = keyboard
    return json.dumps(rkbd)


@csrf_exempt
def reg_webhook(request, bot_tg):

    # Получаем словарь из тела полученного вебхука
    try:
        from_tg = json.loads(request.body)
    except Exception:
        from_tg = {}

    # Создаём объект BotData для работы с данными с вебхука
    bot = BotData(bot_tg)

    # Создаём обхект LocalData для работы с базой данных
    local = LocalData(bot_tg, bot.user_id(from_tg))

    # Получаем объект message
    message = bot.get_message(from_tg)

    # Если юзера нет в базе, добавляем в базу и запускаем регистрацию
    if not local.user_is_in_base:
        local.user_new

    text = ''
    answer = {
        'chat_id': local.chat_id,
        'reply_markup': hide_kbrd()
    }
    send_done = False
    state = local.user_state

    # Если нажата кнопка "Администрировать"
    if (bot.get_data_type(from_tg) == 'text' and
            message.get('text') == 'Администрировать'
            and not local.temp_admin_new):
        pin = str(uuid1())
        BotAdmin.objects.filter(chat=local.chat_id).update(pin=pin)
        text = 'Для входа в админпанель нажмите кнопку:'
        answer['reply_markup'] = admin_kbrd(local.chat_id, pin)

    # Если нажата кнопка "Техподдержка"
    elif (bot.get_data_type(from_tg) == 'text' and
            message.get('text') == 'Техподдержка'
            and not local.temp_admin_new):
        local.user_edit(state='support')
        text = '''Сообщите, о каком боте идет речь и суть проблемы.
        Пишите сообщение в техподдержку (только текст):'''

    # Если нажата кнопка "Сообщение админам"
    elif (bot.get_data_type(from_tg) == 'text' and
            message.get('text') == 'Сообщение админам'
            and not local.temp_admin_new):
        local.user_edit(state='message_to_admins')
        text = 'Пишите (только текст):'

    # Принимаем от пользователя регистрационную информацию
    elif (bot.get_data_type(from_tg) == 'text'
            and state == ''
            or state == 'start'):
        if local.temp_admin_new:
            local.user_edit(state='get_admin_first_name')
            text = '''Приветствую вас!
                Вы беседуете с ботом платформы StudyBot.Fun.
                Для отправки заявки надо пройти 5 простых шагов.

                Шаг 1. Введите Ваше имя (только Имя):'''
        else:
            text = 'Вы уже являетесь администраторм ботов!'
            answer['reply_markup'] = main_kbrd(local.chat_id)
            local.user_edit(state='')

    elif state == 'get_admin_first_name':
        if message.get('text'):
            text = '''Хорошо!

            Шаг 2. Введите вашу Фамилию (только Фамилию):'''
            local.temp_admin_edit(first_name=message['text'])
            local.user_edit(
                first_name=message['text'],
                state='get_admin_last_name')
        else:
            text = 'Шаг 1. Введите Ваше имя (только Имя):'

    elif state == 'get_admin_last_name':
        if message.get('text'):
            text = '''Отлично!

            Шаг 3. Ведите организацию, в которой вы работаете:'''
            local.temp_admin_edit(last_name=message['text'])
            local.user_edit(
                state='get_admin_org',
                last_name=message['text'])
        else:
            text = 'Шаг 2. Введите вашу Фамилию (только Фамилию):'

    elif state == 'get_admin_org':
        if message.get('text'):
            text = '''Ещё немного :)

            Шаг 4. Введите вашу должность:'''
            local.temp_admin_edit(org=message['text'])
            local.user_edit(state='get_admin_position')
        else:
            text = 'Шаг 3. Ведите организацию, в которой вы работаете:'

    elif state == 'get_admin_position':
        if message.get('text'):
            text = '''И последнее....

            Шаг 5. Объясните в 3-х предложениях, 
    зачем вам этот бот, 
    для чего будете его использовать:'''
            local.temp_admin_edit(position=message['text'])
            local.user_edit(state='get_admin_why')
        else:
            text = 'Шаг 4. Введите вашу должность:'

    elif state == 'get_admin_why':
        if message.get('text'):
            text = '''Спасибо за информацию.
            Данные были отправлены супербоссу :)
            После его подтверждения, вы сможете работать на платформе.'''
            local.temp_admin_edit(why=message['text'])
            local.user_edit(state='')
            temp_admin = Temp.objects.get(chat=local.chat_id)
            temp_user = Spisok.objects.get(chat=local.chat_id)
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

    # Статус "Сообщение админам"- принимаем текст для всех админов от Супербосса"
    elif state == 'message_to_admins':
        if message.get('text') and message.get('text') != 'Сообщение админам':
            text = 'Сообщение от СуперБосса:\n'
            admins = local.all_admins_bots
            for chat_id in admins:
                answer = {
                    'chat_id': chat_id,
                    'text': f"{text}{message['text']}",
                    'reply_markup': reply_kbrd(local.chat_id),
                }
                bot.send_answer(answer)
            answer = {
                'chat_id': local.chat_id,
                'text': 'Сообщение отправлено',
            }
            bot.send_answer(answer)
            local.user_edit(state='')
            send_done = True
        elif message['text'] != 'Сообщение админам':
            text = 'Сообщение не отправлено. Можно отправлять ТОЛЬКО тексты!',

    # Статус "Техподдержка"- принимаем текст от админа для Супербосса"
    elif state == 'support':
        if message.get('text') and message.get('text') != 'Техподдержка':
            cur_user = Spisok.objects.get(chat=local.chat_id)
            text = ('Сообщение от админа: '
                    f'{cur_user.first_name} {cur_user.last_name}\n'
                    f'id: {cur_user.id}; chat-id: {cur_user.chat}\n\n')
            answer = {
                'chat_id': settings.BIG_BOSS_ID,
                'text': f"{text}{message['text']}",
                'reply_markup': reply_kbrd(local.chat_id),
            }
            bot.send_answer(answer)
            answer = {
                'chat_id': local.chat_id,
                'text': 'Сообщение отправлено',
            }
            bot.send_answer(answer)
            local.user_edit(state='')
            send_done = True
        elif message['text'] != 'Техподдержка':
            text = 'Сообщение не отправлено. Можно отправлять ТОЛЬКО тексты!',

    # Статус "Ответить"- принимаем текст в ответ в переписке"
    elif 'reply' in state:
        if message.get('text'):
            chat_id = state.split(':')[1]
            text = f'Сообщение от: {local.user_full_name}\n\n'
            answer = {
                'chat_id': chat_id,
                'text': f"{text}{message['text']}",
                'reply_markup': reply_kbrd(local.chat_id),
            }
            bot.send_answer(answer)
            answer = {
                'chat_id': local.chat_id,
                'text': 'Сообщение отправлено',
            }
            bot.send_answer(answer)
            local.user_edit(state='')
            send_done = True
        else:
            text = 'Сообщение не отправлено. Можно отправлять ТОЛЬКО тексты!',

    # Если супербосс нажал "Одобрить/Отклонить"
    elif bot.get_data_type(from_tg) == 'callback_query':
        callback_query = from_tg['callback_query']['data']
        callback = callback_query.split(':')
        answer['chat_id'] = callback[1]

        # Если нажата кнопка "Одобрить"
        if callback[0] == 'approve':
            temp_user = Temp.objects.get(chat=callback[1])
            try:
                BotAdmin.objects.create(
                    chat=callback[1],
                    first_name=temp_user.first_name,
                    last_name=temp_user.last_name,
                    cur_bot=1
                )
            except Exception as exc:
                print(exc)
            Spisok.objects.filter(chat=callback[1]).update(
                first_name=temp_user.first_name,
                last_name=temp_user.last_name,
            )
            Temp.objects.filter(chat=callback[1]).delete()
            answer['reply_markup'] = main_kbrd(local.chat_id)
            text = '''Ваша заявка одобрена.

                На клавиатуре нажмите кнопу "Администрировать",
                чтобы пройти в административную панель.'''
            text_to_boss = 'Отправлено одобрение'

        # Если нажата кнопка "Отклонить"
        elif callback[0] == 'reject':
            Temp.objects.filter(chat=callback[1]).delete()
            Spisok.objects.filter(chat=callback[1]).delete()
            text = 'Ваша заявка отклонена!.'
            answer['reply_markup'] = hide_kbrd()
            text_to_boss = 'Отправлен отказ'

        # Если нажата кнопка "Ответить"
        elif callback[0] == 'reply':
            local.user_edit(state=f'reply:{callback[1]}')
            send_user = Spisok.objects.get(chat=callback[1])
            text = (f'Отправьте ваш ответ (только текст). Его получит '
                    f'{send_user.first_name} {send_user.last_name}'),

        answer_to_boss = {
            'chat_id': settings.BIG_BOSS_ID,
            'text': text_to_boss,
        }
        bot.send_answer(answer_to_boss)

        answer_to_boss = {
            'chat_id': settings.BIG_BOSS_ID,
            'text': text_to_boss,
        }
        bot.send_answer(answer_to_boss)

    if not send_done:
        answer['text'] = text
        bot.send_answer(answer)

    return render(request, 'webhook/123.html')
