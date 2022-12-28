from bots.models import Bot, BotAdmin
from groups.models import Group
from kr.models import KR
from plans.models import Plan

IGNORE_URL = ('/webhook/', '/admin')


def verify_url(path):
    for url in IGNORE_URL:
        if url in path:
            return False
    return True


def get_context(request):
    if not verify_url(request.path):
        return {}
    
    context = get_admin(request)
    data = request.path.split('/')
    context = context | get_bot(data)
    if len(data) > 2:
        context = context | get_plan(request.path, data)
        context = context | get_group(request.path, data)
        context = context | get_kr(request.path, data)
    context = context | get_crumbs(request.path, context)
    return context


def get_admin(request):
    chat = request.COOKIES.get('chatid')
    admin = BotAdmin.objects.get(chat=chat)
    return {
        'first_name': admin.first_name,
        'last_name': admin.last_name,
    }


def get_bot(data):
    if not (data[1] == 'bot' and data[2].isdigit()):
        return {}
    botid =  int(data[2])
    bot = Bot.objects.get(id=botid)
    return {
        'botid': botid,
        'bot_name': bot.name,
        'bot_password': bot.password,
        'bot_login': bot.login[1:],
    }


def get_plan(path, data):
    if not ('/plan/' in path and data[3] == 'plan' and data[4].isdigit()):
        return {}
    planid = int(data[4])
    plan = Plan.objects.get(id=planid)
    return {
        'plan_id': planid,
        'plan_name': plan.name,
    }


def get_group(path, data):
    if not ('/group/' in path and data[3] == 'group' and data[4].isdigit()):
        return {}
    groupid = int(data[4])
    group = Group.objects.get(id=groupid)
    return {
        'group_id': groupid,
        'group_name': group.name,
        'group_pin': group.pin,
    }


def get_kr(path, data):
    if not ('/kr/' in path and data[3] == 'kr' and data[4].isdigit()):
        return {}
    krid = int(data[4])
    kr = KR.objects.get(id=krid)
    return {
        'kr_id': krid,
        'kr_name': kr.name,
        'kr_item': kr.item_id,
    }


def get_crumbs(path, context):
    crumbs = [{'text': 'Все боты', 'url': '/'}]
    if 'botid' in context:
        url = f'/bot/{ context["botid"] }/'
        cr = ({'text': f'Бот "{ context["bot_name"] }"', 'url': url})
        crumbs.append(cr)
    if 'plan_id' in context:
        url += 'plan/'
        cr = ({'text': 'Все планы', 'url': url})
        crumbs.append(cr)
        url += f'{ context["plan_id"] }/'
        cr = ({'text': f'План "{ context["plan_name"] }"', 'url': url})
        crumbs.append(cr)
    elif 'group_id' in context:
        url += 'group/'
        cr = ({'text': 'Все группы', 'url': url})
        crumbs.append(cr)
        url += f'{ context["group_id"] }/'
        cr = ({'text': f'Группа "{ context["group_name"] }"', 'url': url})
        crumbs.append(cr)
    elif 'kr_id' in context:
        url += 'kr/'
        cr = ({'text': 'Все КР', 'url': url})
        crumbs.append(cr)
        url += f'{ context["kr_id"] }/'
        cr = ({'text': f'КР "{ context["kr_name"] }"', 'url': url})
        crumbs.append(cr)
    elif '/works/' in path:
        url += 'works/'
        cr = ({'text': 'Работы учащихся', 'url': url})
        crumbs.append(cr)
    return {'crumbs': crumbs, }
