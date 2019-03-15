from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

# app_name = 'FruitSalesMgmt'
urlpatterns = [
    path('', views.top, name='top'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('fruits', views.fruits_list, name='fruits_list'),
    path('fruits/create', views.fruits_create, name='fruits_create'),
    path('fruits/<pk>/edit', views.fruits_edit, name='fruits_edit'),
    path('fruits/<pk>/remove', views.fruits_remove, name='fruits_remove'),
    path('sales', views.sales_list, name='sales_list'),
    path('sales/create', views.sales_create, name='sales_create'),
    path('sales/<pk>/edit', views.sales_edit, name='sales_edit'),
    path('sales/<pk>/remove', views.sales_remove, name='sales_remove'),
    path('stats', views.stats, name='stats'),
]
