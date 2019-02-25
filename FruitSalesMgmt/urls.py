from django.urls import path
from . import views

urlpatterns = [
    path('', views.top, name='top'),
    path('fruits', views.fruits_list, name='fruits_list'),
    path('sales', views.sales_list, name='sales_list'),
    path('stats', views.stats, name='stats'),
]
