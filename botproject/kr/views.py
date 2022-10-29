import random

from bots.models import Bot
from edubot.main_classes import BotData
from core.utils import add_dir, del_dir, del_file, replace_from_temp
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from edubot.keyboards import push_kr_kbrd
from groups.models import Group, Spisok
from plans.models import Plan, PlanItem

from .forms import KRAdd, TaskAdd
from .models import KR, KROut, Task, TaskOut


def kr_out(request, botid, krid):
    cur_bot = get_object_or_404(Bot, id=botid)
    bot = BotData(cur_bot.tg)
    cur_kr = get_object_or_404(KR, id=krid)
    if request.method != 'POST':
        groups = cur_kr.item.plan.groupplan.all()
        context = {
            'groups': groups,
            'now': timezone.now().strftime('%Y-%m-%dT%H:%M')
        }
        return render(request, 'kr/kr_out.html', context)

    if request.POST['deadline']:
        deadline = request.POST['deadline']
    else:
        deadline = None
    groups = request.POST.getlist('group')
    kr_dict = {}
    for group in groups:
        cur_group = get_object_or_404(Group, id=group)
        kr_out = KROut.objects.create(
            kr=cur_kr,
            group=cur_group,
            deadline=deadline
        )
        kr_dict[group] = kr_out

    chats = request.POST.getlist('chat')
    tasks = cur_kr.task.all()
    tasks_fly = {}
    for i in range(cur_kr.kolzad):
        tasks_fly[i+1] = [task for task in tasks if task.number == i+1]
        for value in chats:
            chat = value.split(':')[0]
            group = value.split(':')[1]
            user = get_object_or_404(Spisok, chat=chat)
            task = random.choice(tasks_fly[i+1])
            line = '-'*70
            if i == 0:
                text = (f'{line}\n<b>КОНТРОЛЬНАЯ РАБОТА</b>\n'
                        f'<b>{cur_kr.name}</b>\n{line}\n')
                answer = {
                    'chat_id': user.chat,
                    'text': text,
                    'parse_mode': 'HTML'
                }
                bot.send_answer(answer)
            TaskOut.objects.create(
                number=i+1,
                task=task,
                krout=kr_dict[group],
                user=user
            )
            k = i + 1
            text = f'<b>Задача № {k}</b>\n{line}\n{task.text}'
            answer = {
                'chat_id': user.chat,
                'text': text,
                'parse_mode': 'HTML'
            }
            bot.send_answer(answer)
            if i + 1 == cur_kr.kolzad:
                cur_item = cur_kr.item
                answer = {
                    'chat_id': user.chat,
                    'text': 'Для сдачи работы нажмите на кнопку:',
                    'reply_markup': push_kr_kbrd(
                        cur_item.id, kr_dict[group].id, group),
                }
                bot.send_answer(answer)

    messages.success(request, 'Контрольная работа отправлена.')
    return redirect('kr:kr', botid=botid, krid=krid)


def index(request, botid):
    krs = KR.objects.filter(bot=botid)
    kr_plan = {}
    for kr in krs:
        cur_kr = get_object_or_404(KR, id=kr.id)
        plan = cur_kr.item.plan
        kr_plan[kr.id] = plan
    context = {
        'widget': 'kr',
        'krs': krs,
        'kr_plan': kr_plan,
    }
    return render(request, 'kr/krs.html', context)


def kr_add(request, botid):
    form = KRAdd(request.POST or None)
    form.fields["item"].queryset = PlanItem.objects.filter(
        type='k', plan_id__in=Plan.objects.filter(bot_id=botid).values_list(
            'id', flat=True)).exclude(id__in=KR.objects.all(
            ).values_list('item', flat=True))
    context = {
        'form': form,
        'is_new': True,
        'widget': 'kr',
    }
    if not form.is_valid():
        if request.method == "POST":
            messages.error(request, ' ')
        return render(request, 'kr/kr_add.html', context)
    new_kr = form.save(commit=False)
    new_kr.bot = Bot.objects.get(id=botid)
    new_kr.save()
    add_dir(botid=botid, num_dir=new_kr.id, type_dir='kr')
    messages.success(request, 'Контрольная работа добавлена.')
    return redirect('kr:kr', botid=botid, krid=new_kr.id)


def kr_edit(request, botid, krid):
    cur_kr = get_object_or_404(KR, id=krid)
    form = KRAdd(request.POST or None, instance=cur_kr)
    form.fields["item"].queryset = PlanItem.objects.filter(
        type='k', plan_id__in=Plan.objects.filter(bot_id=botid).values_list(
            'id', flat=True)).exclude(id__in=KR.objects.all(
            ).values_list('item', flat=True).exclude(item=cur_kr.item_id))
    context = {
        'form': form,
        'is_new': False,
    }
    if form.is_valid():
        form.save()
        messages.success(request, 'Контрольная работа отредактирована.')
        return redirect('kr:index', botid=botid)
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'kr/kr_add.html', context)


def kr(request, botid, krid):
    cur_kr = get_object_or_404(KR, id=krid)
    task_list = cur_kr.task.all()
    tasks = {}
    for i in range(cur_kr.kolzad):
        task_number = []
        for task in task_list:
            if task.number == i+1:
                task_number.append(task)
        tasks[i+1] = task_number
    pulls = cur_kr.kr_out.select_related('group')
    context = {
        'itemid': cur_kr.item.id,
        'tasks': tasks,
        'pulls': pulls,
        'now': timezone.now(),
    }
    return render(request, 'kr/kr.html', context)


def task_del(request, botid, krid, taskid):
    cur_task = Task.objects.get(id=taskid)
    if cur_task.img:
        del_file(url=cur_task.img)
    Task.objects.filter(id=taskid).delete()
    messages.success(request, 'Задача удалена')
    return redirect('kr:kr', botid=botid, krid=krid)


def kr_del(request, botid, krid):
    KR.objects.filter(id=krid).delete()
    messages.success(request, 'Контрольная работа удалена')
    del_dir(botid=botid, num_dir=krid, type_dir='kr')
    return redirect('kr:index', botid=botid)


def task_add(request, botid, krid):
    cur_kr = get_object_or_404(KR, id=krid)
    form = TaskAdd(request.POST, request.FILES, kolzad=cur_kr.kolzad or None)
    context = {
        'form': form,
    }
    if not form.is_valid():
        if request.method == "POST":
            messages.error(request, ' ')
        return render(request, 'kr/task_add.html', context)
    new_task = form.save(commit=False)
    new_task.kr = KR.objects.get(id=krid)
    new_task.save()
    if request.FILES:
        name_new = replace_from_temp(
            botid=botid, num_file=new_task.id, type_dir='kr',
            num_dir=krid, img_name=request.FILES['img']._name)
        Task.objects.filter(id=new_task.id).update(
            img='/'.join([str(botid), 'kr'+str(krid), name_new]))
    messages.success(request, 'Задача добавлена.')
    return redirect('kr:kr', botid=botid, krid=krid)


def task_edit(request, botid, krid, taskid):
    cur_task = get_object_or_404(Task, id=taskid)
    img_url = cur_task.img
    cur_kr = get_object_or_404(KR, id=krid)
    context = {
        'numbers': (i + 1 for i in range(cur_kr.kolzad)),
        'cur_task': cur_task,
    }
    if request.method != 'POST':
        if request.method == "POST":
            messages.error(request, ' ')
        return render(request, 'kr/task_edit.html', context)
    form = TaskAdd(request.POST, request.FILES,
                   kolzad=cur_kr.kolzad, instance=cur_task)
    if not form.is_valid():
        return render(request, 'kr/task_edit.html', context)
    if request.FILES and img_url or request.POST.get('img-clear', False):
        del_file(url=img_url)
    form.save()
    if request.FILES:
        name_new = replace_from_temp(
            botid=botid, num_file=taskid, type_dir='kr',
            num_dir=krid, img_name=request.FILES['img']._name)
        Task.objects.filter(id=taskid).update(
            img='/'.join([str(botid), 'kr'+str(krid), name_new]))
    messages.success(request, 'Задача отредактирована.')
    return redirect('kr:kr', botid=botid, krid=krid)
