from django.urls import path

from . import views

app_name = 'plans'

urlpatterns = [
    path('<int:planid>/item/<int:itemid>/del',
         views.item_del, name='item_del'),

    path('<int:planid>/item/<int:itemid>/edit',
         views.item_edit, name='item_edit'),

    path('<int:planid>/additem/',
         views.item_add, name='item_add'),

    path('<int:planid>/attachgroup/',
         views.plan_attach_group, name='plan_attach_group'),

    path('<int:planid>/order/',
         views.plan_order, name='plan_order'),

    path('<int:planid>/edit/',
         views.plan_edit, name='plan_edit'),

    path('<int:planid>/del/',
         views.plan_del, name='plan_del'),

    path('<int:planid>/',
         views.plan_items, name='plan_items'),

    path('add/', views.plan_add, name='plan_add'),

    path('', views.index, name='index'),
]
