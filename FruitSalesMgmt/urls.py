from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# app_name = 'FruitSalesMgmt'
urlpatterns = [
    path('', views.top, name='top'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('fruits', views.fruits_list, name='fruits_list'),
    path('fruits/new', views.fruits_new, name='fruits_new'),
    path('fruits/<pk>/edit', views.fruits_edit, name='fruits_edit'),
    path('fruits/<pk>/remove', views.fruits_remove, name='fruits_remove'),
    path('sales', views.sales_list, name='sales_list'),
    path('sales/new', views.sales_new, name='sales_new'),
    path('sales/<pk>/edit', views.sales_edit, name='sales_edit'),
    path('sales/<pk>/remove', views.sales_remove, name='sales_remove'),
    path('stats', views.stats, name='stats'),
]
