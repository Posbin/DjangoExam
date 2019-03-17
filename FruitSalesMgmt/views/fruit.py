from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import FruitForm
from ..models import Fruit


@login_required
def fruits_list(request):
    fruits = Fruit.objects.all().order_by('-id')
    return render(request, 'FruitSalesMgmt/fruits_list.html',
                  {'fruits': fruits})


@login_required
def fruits_create(request):
    if request.method == "POST":
        form = FruitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fruits_list')
    else:
        form = FruitForm()
    return render(request, 'FruitSalesMgmt/fruits_edit.html', {'form': form})


@login_required
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


@login_required
def fruits_remove(request, pk):
    fruit = get_object_or_404(Fruit, pk=pk)
    fruit.delete()
    return redirect('fruits_list')
