import csv
from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import SaleForm, SalesDataUploadForm
from ..models import Fruit, Sale

"""
販売情報管理
"""


@login_required
def sales_list(request):
    """
    一覧画面
    """
    uploaded_message = ''
    if request.method == "POST":
        upload_form = SalesDataUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            message = 'CSVファイルからの読み込みを完了しました。\
                      （登録成功: {0}件, 登録失敗: {1}件）'
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
    """
    CSVファイルを読み込んで販売情報の登録を行う。
    登録処理の成功数、失敗数を戻り値として返す。

    :param f: CSVファイル
    :type f: UploadedFile
    :returns: 登録処理の成功数、失敗数
    :rtype: (int, int)
    """
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
    """
    CSVファイルの各行の値を渡して、販売情報データに変換する。
    変換できない場合は、Noneを返す。

    :param row: CSVファイルの各行
    :type row: list
    :returns: 販売情報データ
    :rtype: Sale
    """
    if len(row) != 4:
        return None
    time_zone = pytz.timezone(settings.TIME_ZONE)
    try:
        dt = datetime.strptime(row[3], '%Y-%m-%d %H:%M')
        sale = Sale(
            fruit=Fruit.objects.get(name=row[0]),
            number=int(row[1]),
            total=int(row[2]),
            datetime=dt.astimezone(time_zone)
        )
        return sale
    except (Fruit.DoesNotExist, ValueError):
        return None


@login_required
def sales_create(request):
    """
    販売情報追加
    """
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
    """
    編集
    """
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
    """
    削除
    """
    sale = get_object_or_404(Sale, pk=pk)
    sale.delete()
    return redirect('sales_list')
