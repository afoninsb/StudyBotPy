from django.urls import path

from . import views

app_name = 'bots'

urlpatterns = [
    path('bot/<int:botid>/botadmins/', views.botadmins, name='bot_admins'),
    path('bot/<int:botid>/addadmin/', views.botaddadmin, name='bot_addadmin'),
    path('bot/<int:botid>/del/', views.botdel, name='bot_del'),
    path('bot/<int:botid>/edit/', views.botedit, name='bot_edit'),
    path('bot/<int:botid>/pass/', views.botpass, name='bot_pass'),
    path('bot/<int:botid>/', views.bot, name='bot_page'),
    path('bot/add/', views.botadd, name='bot_add'),
    path('', views.index, name='index'),
]
