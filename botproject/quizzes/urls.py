from django.urls import path

from . import views

app_name = 'quizzes'

urlpatterns = [
    path('add/<int:step>/', views.quiz_add, name='quiz_add'),
]
