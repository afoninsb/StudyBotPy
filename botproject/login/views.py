from bots.models import BotAdmin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def enter(request, chatid, pin):
    """Авторизация администратора в панели."""
    if request.COOKIES.get('chatid'):
        response = HttpResponse("Cookie deleted")
        response.delete_cookie("chatid")
    try:
        BotAdmin.objects.get(chat=chatid, pin=pin)
        BotAdmin.objects.filter(chat=chatid).update(pin='')
        response = HttpResponseRedirect(reverse('bots:index'))
        response.set_cookie(
            key='chatid',
            value=chatid,
            secure=True,
            max_age=36000)
    except ObjectDoesNotExist:
        mess = '<center><h2>Неизвестный пользователь</h2></center>'
        response = HttpResponse(mess)
    return response


def logout(request):
    """Выход администратора."""
    response = HttpResponse('<center><h2>До свидания!</h2></center>')
    response.delete_cookie("chatid")
    return response
