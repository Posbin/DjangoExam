from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def top(request):
    return render(request, 'FruitSalesMgmt/top.html')
