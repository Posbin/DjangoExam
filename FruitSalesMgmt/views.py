from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from .models import Fruit, Sale
from .forms import FruitForm, SaleForm

def top(request):
    return render(request, 'FruitSalesMgmt/top.html', {})

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
    monthly_stats = get_monthly_stats(5)
    daily_stats = get_daily_stats(5)
    return render(request, 'FruitSalesMgmt/stats.html', {'all_stats_total': all_stats.total, 'monthly_stats': monthly_stats, 'daily_stats': daily_stats})

def get_monthly_stats(num):
    ago = num - 1
    today = timezone.now()
    begin_date = (today - relativedelta(months=ago)).replace(day=1)        
    stats = get_init_monthly_stats(begin_date, today)

    sales = Sale.objects.filter(datetime__gte=begin_date)
    for sale in sales:
        key = sale.datetime.strftime('%y/%m')
        stats[key].append_sale_data(sale)
    return stats

def get_daily_stats(num):
    ago = num - 1
    today = timezone.now()
    begin_date = today - timedelta(days=ago)
    stats = get_init_daily_stats(begin_date, today)

    sales = Sale.objects.filter(datetime__gte=begin_date)
    for sale in sales:
        key = sale.datetime.strftime('%y/%m/%d')
        stats[key].append_sale_data(sale)
    return stats

def get_init_daily_stats(from_date, to_date):
    stats = {}
    date_i = from_date
    while date_i <= to_date:
        key = '{0}/{1}/{2}'.format(date_i.year, date_i.month, date_i.day)
        stats[key] = Stat()
        date_i += timedelta(days=1)
    return stats

def get_init_monthly_stats(from_date, to_date):
    stats = {}
    date_i = from_date
    while date_i <= to_date:
        key = '{0}/{1}'.format(date_i.year, date_i.month)
        stats[key] = Stat()
        date_i += relativedelta(months=1)
    return stats

class Stat:
    def __init__(self, sales=[]):
        self.sales = sales

    def append_sale_data(self, sale):
        self.sales.append(sale)
    
    @property
    def details(self):
        details_list = [detail(sale) for sale in self.sales]
        return ', '.join(details_list)

    def detail(sale):
        return '{0}: {1}円({2})'.format(sale.name, sale.total, sale.number)

    @property
    def total(self):
        return sum([sale.total for sale in self.sales])
