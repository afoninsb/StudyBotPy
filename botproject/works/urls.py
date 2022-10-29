from django.urls import path

from . import views

app_name = 'works'

urlpatterns = [
    path('panel/<str:work>/<str:razdel>/<int:id>/<int:itemid>/<str:verified>/<int:idworks>/',
         views.panel_stat, name='panel_stat'),
    path('', views.panel, name='panel'),
]
