from bots.models import Bot
from core.utils import handle_uploaded_file
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from edubot.main_classes import BotData
from groups.models import Group, Spisok


def send_message_to_user(request, botid, userid):
    cur_bot = get_object_or_404(Bot, id=botid)
    bot = BotData(cur_bot.tg)
    cur_user = get_object_or_404(Spisok, id=userid)
    if request.method != 'POST':
        context = {
            'user': cur_user,
        }
        return render(request, 'message/send_message_user.html', context)
    answer = {
        'chat_id': cur_user.chat,
        'text': request.POST['text'],
    }
    bot.send_answer(answer)
    if request.FILES:
        img = handle_uploaded_file(request.FILES['img'])
        url = (
            settings.BASE_URL +
            settings.TEMP_URL +
            img
        )
        data = {
            'chat_id': cur_user.chat,
            'photo': url,
        }
        bot.send_photo(data)
    messages.success(request, 'Сообщение отправлено.')
    return redirect(
        'message:send_message_user', botid=botid, userid=cur_user.id
    )


def send_message_to_group(request, botid):
    cur_bot = get_object_or_404(Bot, id=botid)
    bot = BotData(cur_bot.tg)
    if request.method != 'POST':
        groups = (
            Group.objects.prefetch_related('users').
            filter(bot__id=botid)
        )
        context = {
            'groups': groups,
        }
        return render(request, 'message/send_message_group.html', context)
    chats = request.POST.getlist('chat')
    if request.FILES:
        img = handle_uploaded_file(request.FILES['img'])
    for chat in chats:
        answer = {
            'chat_id': chat,
            'text': request.POST['text'],
        }
        bot.send_answer(answer)
        if request.FILES:
            url = (
                settings.BASE_URL +
                settings.TEMP_URL +
                img
            )
            data = {
                'chat_id': chat,
                'photo': url,
            }
            bot.send_photo(data)
    messages.success(request, 'Сообщение отправлено.')
    return redirect('message:send_message_group', botid=botid)
