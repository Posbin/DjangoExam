from django.shortcuts import render

def top(request):
    return render(request, 'FruitSalesMgmt/top.html', {})

def fruits_list(request):
    return render(request, 'FruitSalesMgmt/fruits_list.html', {})

def sales_list(request):
    return render(request, 'FruitSalesMgmt/sales_list.html', {})

def stats(request):
    return render(request, 'FruitSalesMgmt/stats.html', {})
