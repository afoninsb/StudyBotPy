from django.urls import path

from . import views

app_name = 'message'

urlpatterns = [
    path('<int:userid>/', views.send_message_to_user, name='send_message_user'),
    path('', views.send_message_to_group, name='send_message_group'),
]
