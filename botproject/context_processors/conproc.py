from bots.models import Bot, BotAdmin
from groups.models import Group
from kr.models import KR
from plans.models import Plan


def get_admin(request):
    if '/tgbot_backend/' not in request.path and '/webhook/' not in request.path:       
        chat = request.COOKIES.get('chatid')
        admin = BotAdmin.objects.get(chat=chat)
        return {
            'first_name': admin.first_name,
            'last_name': admin.last_name,
        }
    return {}


def get_bot_id(request):
    data = request.path.split('/')
    if data[1] == 'bot' and data[2].isdigit():
        return {'bot_id': int(data[2]), }
    return {}


def get_bot(request):
    data = get_bot_id(request)
    if data:
        bot = Bot.objects.get(id=data['bot_id'])
        return {
            'botid': bot.id,
            'bot_name': bot.name,
            'bot_password': bot.password,
            'bot_login': bot.login[1:],
        }
    return {}


def get_plan(request):
    if '/plan/' in request.path and '/tgbot_backend/' not in request.path:
        data = request.path.split('/')
        if len(data) > 2:
            if data[3] == 'plan' and data[4].isdigit():
                planid = int(data[4])
                plan = Plan.objects.get(id=planid)
                return {
                    'plan_id': planid,
                    'plan_name': plan.name,
                }
    return {}


def get_group(request):
    if '/group/' in request.path:
        data = request.path.split('/')
        if len(data) > 2:
            if data[3] == 'group' and data[4].isdigit():
                groupid = int(data[4])
                group = Group.objects.get(id=groupid)
                return {
                    'group_id': groupid,
                    'group_name': group.name,
                    'group_pin': group.pin,
                }
    return {}


def get_kr(request):
    if '/kr/' in request.path:
        data = request.path.split('/')
        if len(data) > 2:
            if data[3] == 'kr' and data[4].isdigit():
                krid = int(data[4])
                kr = KR.objects.get(id=krid)
                return {
                    'kr_id': krid,
                    'kr_name': kr.name,
                    'kr_item': kr.item_id,
                }
    return {}


def get_crumbs(request):
    crumbs = [{'text': 'Все боты', 'url': '/'}]
    bot = get_bot(request)
    plan = get_plan(request)
    group = get_group(request)
    kr = get_kr(request)
    if bot:
        url = f'/bot/{ bot["botid"] }/'
        cr = ({'text': f'Бот "{ bot["bot_name"] }"', 'url': url})
        crumbs.append(cr)
    if plan:
        url += 'plan/'
        cr = ({'text': 'Все планы', 'url': url})
        crumbs.append(cr)
        url += f'{ plan["plan_id"] }/'
        cr = ({'text': f'План "{ plan["plan_name"] }"', 'url': url})
        crumbs.append(cr)
    elif group:
        url += 'group/'
        cr = ({'text': 'Все группы', 'url': url})
        crumbs.append(cr)
        url += f'{ group["group_id"] }/'
        cr = ({'text': f'Группа "{ group["group_name"] }"', 'url': url})
        crumbs.append(cr)
    elif kr:
        url += 'kr/'
        cr = ({'text': 'Все КР', 'url': url})
        crumbs.append(cr)
        url += f'{ kr["kr_id"] }/'
        cr = ({'text': f'КР "{ kr["kr_name"] }"', 'url': url})
        crumbs.append(cr)
    elif '/works/' in request.path:
        url += 'works/'
        cr = ({'text': 'Работы учащихся', 'url': url})
        crumbs.append(cr)
    return {'crumbs': crumbs, }
