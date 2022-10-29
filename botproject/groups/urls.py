from django.urls import path

from . import views

app_name = 'groups'

urlpatterns = [
    path('<int:groupid>/deattach_user/<int:userid>/',
         views.group_del_attach_user, name='group_user_deattach'),
    path('<int:groupid>/deattach_plan/<int:planid>/',
         views.group_del_attach_plan, name='group_plan_deattach'),
    path('student/<int:userid>/del/', views.del_student_from_bot,
         name='user_del'),
    path('<int:groupid>/attachplan/', views.group_attach_plan,
         name='group_attach_plan'),
    path('<int:groupid>/addstudent/', views.group_add_user,
         name='group_add_student'),
    path('<int:groupid>/pin/', views.group_pin, name='group_pin'),
    path('<int:groupid>/edit/', views.group_edit, name='group_edit'),
    path('<int:groupid>/del/', views.group_del, name='group_del'),
    path('<int:groupid>/', views.group, name='group'),
    path('add/', views.group_add, name='group_add'),
    path('spisok/', views.spisok, name='spisok'),
    path('', views.index, name='index'),
]
