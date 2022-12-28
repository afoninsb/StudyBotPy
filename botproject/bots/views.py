from core.utils import add_dir, del_dir
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from groups.models import Spisok
from edubot.main_classes import BotData
from bots.forms import AddAdmin, BotForm, BotEditForm, BotPass
from bots.models import Bot, BotAdmin


def index(request):
    """Главная страница панели - боты пользователя."""
    cur_admin = get_object_or_404(BotAdmin, chat=request.COOKIES.get('chatid'))
    bots = cur_admin.bot.all()
    return render(request, 'index.html', {'bots': bots, })

    
def bot(request, botid):
    """Главная страница бота."""
    BotAdmin.objects.filter(
        chat=request.COOKIES.get('chatid')).update(cur_bot=botid)
    return render(request, 'bots/bots.html')


def botadmins(request, botid):
    """Администраторы бота."""
    cur_bot = get_object_or_404(Bot, id=botid)
    admins = cur_bot.admins.all()
    return render(request, 'bots/botadmins.html', {'admins': admins, })


def botaddadmin(request, botid):
    """Добавление администратора бота."""
    if request.method != "POST":
        botadmin = get_object_or_404(
            BotAdmin,
            chat=request.COOKIES.get('chatid')
        )
        form = AddAdmin(
            initial={'cur_bot': botadmin.cur_bot})
        return render(request, 'bots/botaddadmin.html', {'form': form, })
    form = AddAdmin(request.POST)
    if not form.is_valid():
        messages.error(request, ' ')
        return render(request, 'bots/botaddadmin.html', {'form': form, })
    this_bot = Bot.objects.get(id=botid)
    this_bot.admins.add(BotAdmin.objects.get(
        chat=request.POST['tgid']))
    messages.success(request, 'К боту добавлен администратор.')
    return redirect('bots:bot_admins', botid=botid)


def botdel(request, botid):
    """Удаление бота."""
    cur_bot = get_object_or_404(Bot, id=botid)
    bot = BotData(cur_bot.tg)
    bot.delete_webhook()
    cur_bot.delete()
    messages.success(request, 'Бот удалён')
    del_dir(botid=botid, type_dir='bot')
    return redirect('bots:index')


def botpass(request, botid):
    """Установка пароля бота."""
    if request.method != "POST":
        return render(request, 'bots/botpass.html', {'form': BotPass, })
    Bot.objects.filter(id=botid).update(password=request.POST['password'])
    messages.success(request, 'Пароль бота установлен.')
    return redirect('bots:bot_page', botid=botid)


def botedit(request, botid):
    """Редактирование бота."""
    cur_bot = get_object_or_404(Bot, id=botid)
    form = BotEditForm(request.POST or None, instance=cur_bot)
    if not form.is_valid():
        if request.method == "POST":
            messages.error(request, ' ')
        return render(request, 'bots/botadd.html', {'form': form, })
    form.save()
    messages.success(request, 'Бот отредактирован.')
    return redirect('bots:bot_page', botid=botid)


def botadd(request):
    """Добавление бота."""
    form = BotForm(request.POST or None)
    if not form.is_valid():
        context = {
            'form': form,
            'is_new': True,
        }
        if request.method == "POST":
            messages.error(request, ' ')
        return render(request, 'bots/botadd.html', context)
    new_bot = form.save(commit=False)
    new_bot.id = int((request.POST['tg'].split(':'))[0])
    form.save()
    botadmin = get_object_or_404(BotAdmin, chat=request.COOKIES.get('chatid'))
    botadmin.bot.add(new_bot)
    cur_user = get_object_or_404(Spisok, chat=request.COOKIES.get('chatid'))
    cur_user.bots.add(new_bot)
    add_dir(botid=new_bot.id)
    add_dir(botid=new_bot.id, type_dir='works')
    messages.success(request, 'Бот добавлен.')
    return redirect('bots:bot_page', botid=new_bot.id)
