from django.urls import path

from . import views

app_name = 'kr'

urlpatterns = [
    path('<int:krid>/task_edit/<int:taskid>/',
         views.task_edit, name='task_edit'),
    path('<int:krid>/task_del/<int:taskid>/', views.task_del, name='task_del'),
    path('<int:krid>/out/', views.kr_out, name='kr_out'),
    path('<int:krid>/task_add/', views.task_add, name='task_add'),
    path('<int:krid>/del/', views.kr_del, name='kr_del'),
    path('<int:krid>/edit/', views.kr_edit, name='kr_edit'),
    path('<int:krid>/', views.kr, name='kr'),
    path('add/', views.kr_add, name='kr_add'),
    path('', views.index, name='index'),
]
