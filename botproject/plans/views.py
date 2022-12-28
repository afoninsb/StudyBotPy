from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from groups.models import Group
from kr.models import KR

from plans.forms import AddItem, AddPlan, EditItem
from plans.models import Plan, PlanItem


def index(request, botid):
    """Список тематических планов бота."""
    plans = Plan.objects.filter(bot_id=botid).values()
    groups = Group.objects.filter(bot_id=botid).values()
    plans_groups = {}
    for item_plan in plans:
        plan_value = []
        cur_plan = get_object_or_404(Plan, id=item_plan['id'])
        groups_plan = cur_plan.groupplan.all().values()
        for item_group in groups:
            if item_group in groups_plan:
                plan_value.append(item_group)
        plans_groups[item_plan['id']] = plan_value
    context = {
        'plans_groups': plans_groups,
        'plans': plans,
        'widget': 'plan',
    }
    return render(request, 'plans/plans.html', context)


def plan_items(request, botid, planid):
    """Список тем в тематическом плане."""
    items = PlanItem.objects.filter(plan=planid).order_by('weight')
    krs = KR.objects.all()
    kr_item = {kr.item.id: kr.id for kr in krs}
    context = {
        'items': items,
        'kr_item': kr_item,
    }
    return render(request, 'plans/plan_items.html', context)


def plan_del(request, botid, planid):
    """Удаление тематического плана."""
    Plan.objects.filter(id=planid).delete()
    messages.success(request, 'Тематический план удалён!')
    return redirect('plans:index', botid=botid)


def plan_order(request, botid, planid):
    """Сортировка тем в тематическом плане."""
    if request.method != 'POST':
        items = PlanItem.objects.filter(plan=planid).order_by('weight')
        return render(request, 'plans/plan_order.html', {'items': items, })
    ids = request.POST.getlist('ids')
    weights = request.POST.getlist('weights')
    data = dict(zip(ids, weights))
    items = PlanItem.objects.filter(plan=planid)
    for key, value in data.items():
        for item in items:
            if item.id == int(key):
                item.weight = value
                break
    PlanItem.objects.bulk_update(items, ['weight'])
    return redirect('plans:plan_items', botid=botid, planid=planid)


def plan_add(request, botid):
    """Добавялем тематический план."""
    form = AddPlan(request.POST or None)
    if form.is_valid():
        new_plan = form.save(commit=False)
        new_plan.bot_id = botid
        new_plan.save()
        messages.success(request, 'Тематическое планирование создано.')
        return redirect('plans:plan_items', botid=botid, planid=new_plan.id)
    context = {
        'form': form,
        'is_new': True,
        'widget': 'plan',
    }
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'plans/plan_add.html', context)


def plan_edit(request, botid, planid):
    """Редактируем тематический план."""
    cur_plan = get_object_or_404(Plan, id=planid)
    form = AddPlan(request.POST or None, instance=cur_plan)
    if form.is_valid():
        form.save()
        messages.success(request, 'Тематическое планирование отредактировано.')
        return redirect('plans:plan_items', botid=botid, planid=planid)
    context = {
        'form': form,
    }
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'plans/plan_add.html', context)


def item_add(request, botid, planid):
    """Добавляем тему в тематический план."""
    form = AddItem(request.POST or None)
    if form.is_valid():
        new_item = form.save(commit=False)
        if new_item.type == 'k':
            new_item.link = ''
        new_item.plan_id = planid
        new_item.save()
        messages.success(request, 'Тема добавлена в план.')
        return redirect('plans:plan_items', botid=botid, planid=planid)
    context = {
        'form': form,
        'is_new': True,
    }
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'plans/item_add.html', context)


def item_edit(request, botid, planid, itemid):
    """Редактируем тему в тематическом плане."""
    cur_plan = get_object_or_404(Plan, id=planid)
    cur_item = get_object_or_404(PlanItem, id=itemid, plan=cur_plan)
    form = EditItem(request.POST or None, instance=cur_item)
    if form.is_valid():
        form.save()
        messages.success(request, 'Тема отредактирована.')
        return redirect('plans:plan_items', botid=botid, planid=planid)
    context = {
        'form': form,
    }
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'plans/item_add.html', context)


def item_del(request, botid, planid, itemid):
    """Удаляем тему из тематического плана."""
    PlanItem.objects.filter(id=itemid).delete()
    messages.success(request, 'Тема удалена из плана.')
    return redirect('plans:plan_items', botid=botid, planid=planid)


def plan_attach_group(request, botid, planid):
    """Прикрепляем группу к тематическому плану."""
    cur_plan = get_object_or_404(Plan, id=planid)
    if request.method != 'POST':
        groups = Group.objects.filter(bot=botid).exclude(
            id__in=cur_plan.groupplan.all().values_list('id', flat=True))
        context = {
            'groups': groups,
        }
        return render(request, 'plans/attach_group.html', context)
    ids = request.POST.getlist('ids')
    for id in ids:
        cur_plan.groupplan.add(Group.objects.get(id=id))
    return redirect('plans:plan_items', botid=botid, planid=planid)
