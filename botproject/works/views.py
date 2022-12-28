from bots.models import Bot
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from edubot.main_classes import BotData
from groups.models import Group, Spisok
from plans.models import Plan, PlanItem

from .forms import ReviewWork
from .models import Work


def panel_stat(request, botid, **kwargs):
    """Панель по работе ученика."""
    statutes = {
        'passed': 'Сдано',
        'rejected': 'Отклонено',
        'done': 'Зачтено',
    }
    form = ReviewWork()
    if kwargs['idworks'] != 0:
        cur_works = get_object_or_404(
            Work, id=kwargs['idworks'], bot__id=botid)
        form = ReviewWork(request.POST or None, instance=cur_works)
    if form.is_valid():
        form.save()
        messages.success(request, 'Информация сохранена.')
        cur_bot = get_object_or_404(Bot, id=botid)
        cur_user = get_object_or_404(Spisok, id=cur_works.user.id)
        bot = BotData(cur_bot.tg)
        text = f'''
        Ваша работа проверена учителем.
        Статус работы: {statutes[cur_works.status]}
        Оценка: {cur_works.mark}
        Отзыв: {cur_works.review}
        '''
        answer = {
            'chat_id': cur_user.chat,
            'text': text,
        }
        bot.send_answer(answer)
        return redirect(
            'works:panel_stat',
            botid=botid,
            work=kwargs['work'],
            razdel=kwargs['razdel'],
            id=kwargs['id'],
            itemid=kwargs['itemid'],
            verified=kwargs['verified'],
            idworks=0)

    sql = (
        Work.objects.
        filter(bot__id=botid).
        filter(type=kwargs['work']).
        filter(item__id=kwargs['itemid']).
        select_related('user').select_related('item')
    )
    if 'group' in kwargs:
        sql = sql.filter(group__id=kwargs['id']).select_related('group')
    if kwargs['verified'] == 'no':
        sql = sql.filter(~Q(status='done'))
    context = {
        'datas': sql,
        'id': kwargs['id'],
        'razdel': kwargs['razdel'],
        'idworks': kwargs['idworks'],
        'verified': kwargs['verified'],
        'statutes': statutes,
        'form': form
    }
    if request.method == "POST":
        messages.error(request, ' ')
    return render(request, 'works/works.html', context)


def panel(request, botid):
    """Сводная панель по всем работам."""
    plans = Plan.objects.filter(bot_id=botid)
    groups = Group.objects.filter(bot_id=botid).prefetch_related('plans')
    items = PlanItem.objects.filter(type='p')

    p_plans_info = []
    p_p_passed = False
    for plan in plans:
        items_info = []
        for item in items:
            if item.plan_id == plan.id:
                item_temp = {'id': item.id, 'name': item.name}
                if item.link:
                    item_temp['link'] = item.link
                cur_item = get_object_or_404(PlanItem, id=item.id)
                if Work.objects.filter(item=cur_item):
                    item_temp['work_all'] = True
                if Work.objects.filter(item=cur_item).filter(status='passed'):
                    item_temp['work_passed'] = True
                    p_p_passed = True
                items_info.append(item_temp)
        if len(items_info) > 0:
            p_plans_info.append(
                {'id': plan.id, 'name': plan.name, 'items': items_info}
            )

    p_groups_info = []
    p_k_passed = False
    for group in groups:
        items_info = []
        for plan in group.plans.values():
            for item in items:
                if item.plan_id == plan['id']:
                    item_temp = {'id': item.id, 'name': item.name}
                    if item.link:
                        item_temp['link'] = item.link
                    cur_item = get_object_or_404(PlanItem, id=item.id)
                    if Work.objects.filter(item=cur_item).filter(group=group):
                        item_temp['work_all'] = True
                    if (Work.objects
                            .filter(item=cur_item)
                            .filter(status='passed')
                            .filter(group=group)):
                        item_temp['work_passed'] = True
                        p_k_passed = True
                    items_info.append(item_temp)
        if len(items_info) > 0:
            p_groups_info.append(
                {'id': group.id, 'name': group.name, 'items': items_info}
            )

    items = PlanItem.objects.filter(type='k').select_related('kr')

    k_plans_info = []
    k_p_passed = False
    for plan in plans:
        items_info = []
        for item in items:
            if item.plan_id == plan.id:
                item_temp = {'id': item.id, 'name': item.name}
                try:
                    item_temp['link'] = item.kr.id
                except Exception:
                    1 == 1
                cur_item = get_object_or_404(PlanItem, id=item.id)
                if Work.objects.filter(item=cur_item):
                    item_temp['work_all'] = True
                if Work.objects.filter(item=cur_item).filter(status='passed'):
                    item_temp['work_passed'] = True
                    k_p_passed = True
                items_info.append(item_temp)
        if len(items_info) > 0:
            k_plans_info.append(
                {'id': plan.id, 'name': plan.name, 'items': items_info}
            )

    k_groups_info = []
    k_k_passed = False
    for group in groups:
        items_info = []
        for plan in group.plans.values():
            for item in items:
                if item.plan_id == plan['id']:
                    item_temp = {'id': item.id, 'name': item.name}
                    try:
                        item_temp['link'] = item.kr.id
                    except Exception:
                        1 == 1
                    cur_item = get_object_or_404(PlanItem, id=item.id)
                    if Work.objects.filter(item=cur_item).filter(group=group):
                        item_temp['work_all'] = True
                    if (Work.objects
                            .filter(item=cur_item)
                            .filter(status='passed')
                            .filter(group=group)):
                        item_temp['work_passed'] = True
                        k_k_passed = True
                    items_info.append(item_temp)
        if len(items_info) > 0:
            k_groups_info.append(
                {'id': group.id, 'name': group.name, 'items': items_info}
            )

    context = {
        'p_groups_info': p_groups_info,
        'p_plans_info': p_plans_info,
        'k_groups_info': k_groups_info,
        'k_plans_info': k_plans_info,
        'p_p_passed': p_p_passed,
        'p_k_passed': p_k_passed,
        'k_p_passed': k_p_passed,
        'k_k_passed': k_k_passed,
    }
    return render(request, 'works/panel.html', context)
