from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from .models import Fruit, Sale
from .forms import FruitForm, SaleForm

def top(request):
    return render(request, 'FruitSalesMgmt/top.html')

def fruits_list(request):
    fruits = Fruit.objects.all()
    return render(request, 'FruitSalesMgmt/fruits_list.html', {'fruits': fruits})

def fruits_new(request):
    if request.method == "POST":
        form = FruitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fruits_list')
    else:
        form = FruitForm()
    return render(request, 'FruitSalesMgmt/fruits_edit.html', {'form': form})

def fruits_edit(request, pk):
    fruit = get_object_or_404(Fruit, pk=pk)
    if request.method == "POST":
        form = FruitForm(request.POST, instance=fruit)
        if form.is_valid():
            form.save()
            return redirect('fruits_list')
    else:
        form = FruitForm(instance=fruit)
    return render(request, 'FruitSalesMgmt/fruits_edit.html', {'form': form})

def fruits_remove(request, pk):
    fruit = get_object_or_404(Fruit, pk=pk)
    fruit.delete()
    return redirect('fruits_list')

def sales_list(request):
    sales = Sale.objects.all()
    return render(request, 'FruitSalesMgmt/sales_list.html', {'sales': sales})

def sales_new(request):
    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.total = sale.fruit.price * sale.number
            sale.save()
            return redirect('sales_list')
    else:
        form = SaleForm()
    return render(request, 'FruitSalesMgmt/sales_edit.html', {'form': form})

def sales_edit(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == "POST":
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.total = sale.fruit.price * sale.number
            sale.save()
            return redirect('sales_list')
    else:
        form = SaleForm(instance=sale)
    return render(request, 'FruitSalesMgmt/sales_edit.html', {'form': form})

def sales_remove(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    sale.delete()
    return redirect('sales_list')

def stats(request):
    all_sales = Sale.objects.all()
    all_stats = Stat(all_sales)
    monthly_stats = get_monthly_stats(3)
    daily_stats = get_daily_stats(3)

    context = {
        'all_stats_total': all_stats.total,
        'monthly_stats': monthly_stats,
        'daily_stats': daily_stats
    }
    return render(request, 'FruitSalesMgmt/stats.html', context)

def get_monthly_stats(num):
    stats = {}
    ago = num - 1
    today = timezone.now()
    date_i = today
    date_end = today - relativedelta(months=ago)
    while date_i >= date_end:
        year = date_i.year
        month = date_i.month
        key = "{0}/{1}".format(year, month)
        sales = Sale.objects.filter(datetime__year=year,
                                    datetime__month=month)
        stats[key] = Stat(sales)
        date_i -= relativedelta(months=1)
    return stats

def get_daily_stats(num):
    stats = {}
    ago = num - 1
    today = timezone.now()
    date_i = today
    date_end = today - timedelta(days=ago)
    while date_i >= date_end:
        year = date_i.year
        month = date_i.month
        day = date_i.day
        key = "{0}/{1}/{2}".format(year, month, day)
        sales = Sale.objects.filter(datetime__year=year,
                                    datetime__month=month,
                                    datetime__day=day)
        stats[key] = Stat(sales)
        date_i -= timedelta(days=1)
    return stats
    
class Stat:
    def __init__(self, sales):
        self.sales = sales

    @property
    def total(self):
        return sum([sale.total for sale in self.sales])

    @property
    def details(self):
        details_list = [self.__detail(sale) for sale in self.sales]
        return ', '.join(details_list)

    def __detail(self, sale):
        return '{0}: {1}円({2})'.format(sale.fruit.name, sale.total, sale.number)
