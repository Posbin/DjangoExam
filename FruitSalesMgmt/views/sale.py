import csv
from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import SaleForm, SalesDataUploadForm
from ..models import Fruit, Sale


@login_required
def sales_list(request):
    uploaded_message = ''
    if request.method == "POST":
        upload_form = SalesDataUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            message = 'CSVファイルからの読み込みを完了しました。（登録成功: {0}件, 登録失敗: {1}件）'
            success, fail = load_sales_data_from_csv(request.FILES['file'])
            uploaded_message = message.format(success, fail)
    else:
        upload_form = SalesDataUploadForm()
    sales = Sale.objects.select_related().all().order_by('-datetime')
    context = {
        'sales': sales,
        'upload_form': upload_form,
        'uploaded_message': uploaded_message
    }
    return render(request, 'FruitSalesMgmt/sales_list.html', context)


def load_sales_data_from_csv(f):
    success = fail = 0
    decoded_file = f.read().decode('utf-8').splitlines()
    reader = csv.reader(decoded_file)
    for row in reader:
        sale = get_sale_data(row)
        if sale is not None and sale.total > 0:
            sale.save()
            success += 1
        else:
            fail += 1
    return success, fail


def get_sale_data(row):
    if len(row) != 4:
        return None
    time_zone = pytz.timezone(settings.TIME_ZONE)
    try:
        sale = Sale(
            fruit=Fruit.objects.get(name=row[0]),
            number=int(row[1]),
            total=int(row[2]),
            datetime=datetime.strptime(row[3], '%Y-%m-%d %H:%M')
                             .astimezone(time_zone)
        )
        return sale
    except (Fruit.DoesNotExist, ValueError) as e:
        return None


@login_required
def sales_create(request):
    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.total = sale.fruit.price * sale.number
            sale.save()
            return redirect('sales_list')
    else:
        form = SaleForm(initial={'datetime': datetime.now()})
    return render(request, 'FruitSalesMgmt/sales_edit.html', {'form': form})


@login_required
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


@login_required
def sales_remove(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    sale.delete()
    return redirect('sales_list')
