from django.shortcuts import render
from .models import Fruit, Sale

def top(request):
    return render(request, 'FruitSalesMgmt/top.html', {})

def fruits_list(request):
    fruits = Fruit.objects.all()
    return render(request, 'FruitSalesMgmt/fruits_list.html', {'fruits': fruits})

def sales_list(request):
    sales = Sale.objects.all()
    return render(request, 'FruitSalesMgmt/sales_list.html', {'sales': sales})

def stats(request):
    return render(request, 'FruitSalesMgmt/stats.html', {})
