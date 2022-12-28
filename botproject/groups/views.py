from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from faker import Faker

from bots.models import Bot
from groups.forms import AddGroup
from groups.models import Group, Spisok
from plans.models import Plan


def index(request, botid):
    """Группы бота."""
    plans = Plan.objects.filter(bot_id=botid).values()
    groups = Group.objects.filter(bot_id=botid).values()
    groups_plans = {}
    for item_group in groups:
        cur_group = get_object_or_404(Group, id=item_group['id'])
        plans_group = cur_group.plans.all().values()
        group_value = [item_plan for item_plan in plans if item_plan in plans_group]
        groups_plans[item_group['id']] = group_value
    context = {
        'groups_plans': groups_plans,
        'groups': groups,
        'widget': 'group',
    }
    return render(request, 'groups/groups.html', context)


def spisok(request, botid):
    """Список группы."""
    cur_bot = get_object_or_404(Bot, id=botid)
    users = cur_bot.spisok.all()
    context = {
        'users': users,
    }
    return render(request, 'groups/spisok.html', context)


def group(request, botid, groupid):
    """Страница группы."""
    cur_group = get_object_or_404(Group, id=groupid)
    users = cur_group.users.all()
    plans = cur_group.plans.all()
    context = {
        'users': users,
        'plans': plans,
    }
    return render(request, 'groups/group.html', context)


def group_del(request, botid, groupid):
    """Удаляем группу."""
    Group.objects.filter(id=groupid).delete()
    messages.success(request, 'Группа удалена')
    return redirect('groups:index', botid=botid)


def group_add(request, botid):
    """Добавляем группу."""
    form = AddGroup(request.POST or None)
    if form.is_valid():
        new_group = form.save(commit=False)
        new_group.bot_id = botid
        new_group.pin = generate_pin()
        new_group.save()
        messages.success(request, 'Группа добавлена.')
        return redirect('groups:group', botid=botid, groupid=new_group.id)
    context = {
        'form': form,
        'is_new': True,
        'widget': 'group',
    }
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'groups/group_add.html', context)


def group_edit(request, botid, groupid):
    """Редактируем группу."""
    cur_group = get_object_or_404(Group, id=groupid)
    form = AddGroup(request.POST or None, instance=cur_group)
    if form.is_valid():
        form.save()
        messages.success(request, 'Группа отредактирована.')
        return redirect('groups:group', botid=botid, groupid=groupid)
    context = {
        'form': form,
    }
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'groups/group_add.html', context)


def group_pin(request, botid, groupid):
    """Устанавливаем пин-код группе."""
    pin = generate_pin()
    Group.objects.filter(id=groupid).update(pin=pin)
    messages.success(request, 'Группе установлен пин-код '+pin)
    return redirect('groups:group', botid=botid, groupid=groupid)


def generate_pin():
    """Генерируем пин-код группы."""
    fake = Faker()
    pin = str(fake.ean(length=8))
    if Group.objects.filter(pin=pin):
        generate_pin()
    return pin


def del_student_from_bot(request, botid, userid):
    """Удаляем ученика из бота."""
    cur_bot = get_object_or_404(Bot, id=botid)
    cur_user = get_object_or_404(Spisok, id=userid)
    if cur_user.bots.count() > 1:
        cur_bot.spisok.remove(cur_user)
    else:
        Spisok.objects.get(id=userid).delete()
    messages.success(request, 'Ученик удален из бота')
    return redirect('groups:spisok', botid=botid)


def group_del_attach_plan(request, botid, groupid, planid):
    """Открепляем план от группы."""
    cur_plan = get_object_or_404(Plan, id=planid)
    cur_group = get_object_or_404(Group, id=groupid)
    cur_group.plans.remove(cur_plan)
    messages.success(request, 'Тема откреплена от группы')
    return redirect('groups:group', botid=botid, groupid=groupid)


def group_del_attach_user(request, botid, groupid, userid):
    """Удаляем ученика из группы."""
    cur_user = get_object_or_404(Spisok, id=userid)
    cur_group = get_object_or_404(Group, id=groupid)
    cur_group.users.remove(cur_user)
    messages.success(request, 'Ученик удалён из группы')
    return redirect('groups:group', botid=botid, groupid=groupid)


def group_add_user(request, botid, groupid):
    """Добавляем ученика в группу."""
    cur_group = get_object_or_404(Group, id=groupid)
    if request.method != 'POST':
        cur_bot = get_object_or_404(Bot, id=botid)
        users = cur_bot.spisok.all().exclude(
            id__in=cur_group.users.all().values_list('id', flat=True))
        context = {
            'users': users,
        }
        return render(request, 'groups/add_student.html', context)
    ids = request.POST.getlist('ids')
    for id in ids:
        cur_user = get_object_or_404(Spisok, id=id)
        cur_group.users.add(cur_user)
    return redirect('groups:group', botid=botid, groupid=groupid)


def group_attach_plan(request, botid, groupid):
    """Прикрепляем план к группе."""
    cur_group = get_object_or_404(Group, id=groupid)
    if request.method != 'POST':
        plans = Plan.objects.filter(bot=botid).exclude(
            id__in=cur_group.plans.all().values_list('id', flat=True))
        context = {
            'plans': plans,
        }
        return render(request, 'groups/attach_plan.html', context)
    ids = request.POST.getlist('ids')
    for i in range(len(ids)):
        cur_group.plans.add(Plan.objects.get(id=ids[i]))
    return redirect('groups:group', botid=botid, groupid=groupid)
