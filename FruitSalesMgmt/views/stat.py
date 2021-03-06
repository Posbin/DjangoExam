"""
販売統計情報
"""

from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from ..models import Sale


@login_required
def stats(request):
    """
    一覧画面
    """
    all_sales = Sale.objects.select_related().all()
    all_stats = Stat(all_sales)
    monthly_stats = get_monthly_stats(all_sales, 3)
    daily_stats = get_daily_stats(all_sales, 3)

    context = {
        'all_stats_total': all_stats.total,
        'monthly_stats': monthly_stats,
        'daily_stats': daily_stats
    }
    return render(request, 'FruitSalesMgmt/stats.html', context)


def get_monthly_stats(all_sales, num):
    """
    実行時の日時から指定した月数分までの各年月ごとに販売情報を抽出して、
    年月を表す文字列をキー、集計情報（Stat）を値とした辞書で返す。

    :param all_sales: 販売情報のリスト
    :type all_sales: list
    :param num: 取得する月数
    :type num: int
    :returns: 年月を表す文字列をキー、集計情報（Stat）を値とした辞書
    :rtype: dict
    """
    stats = {}
    this_month = timezone.now().date().replace(day=1)
    dates = [this_month - relativedelta(months=ago) for ago in range(num)]
    for date in dates:
        key = '{:%Y/%m}'.format(date)
        sales = list(filter(same_month_filter(date), all_sales))
        stats[key] = Stat(sales)
    return stats


def get_daily_stats(all_sales, num):
    """
    実行時の日時から指定した日数分までの各年月日ごとに販売情報を抽出して、
    年月日を表す文字列をキー、集計情報（Stat）を値とした辞書で返す。

    :param all_sales: 販売情報のリスト
    :type all_sales: list
    :param num: 取得する日数
    :type num: int
    :returns: 年月日を表す文字列をキー、集計情報（Stat）を値とした辞書
    :rtype: dict
    """
    stats = {}
    today = timezone.now().date()
    dates = [today - timedelta(days=ago) for ago in range(num)]
    for date in dates:
        key = '{:%Y/%m/%d}'.format(date)
        sales = list(filter(same_day_filter(date), all_sales))
        stats[key] = Stat(sales)
    return stats


def same_month_filter(date):
    """
    引数で指定した日付の年月と一致するかどうかを判定するラムダ式を返す

    :param date: 判定したい日付
    :type date: date
    :returns: 月判定用ラムダ式
    :rtype: function
    """
    return lambda s: s.datetime.date().replace(day=1) == date


def same_day_filter(date):
    """
    引数で指定した日付の年月日と一致するかどうかを判定するラムダ式を返す

    :param date: 判定したい日付
    :type date: date
    :returns: 日付判定用ラムダ式
    :rtype: function
    """
    return lambda s: s.datetime.date() == date


class Stat:
    """
    販売統計情報ページで表示する集計情報を扱うためのクラス
    """

    def __init__(self, sales):
        """
        :param sales: 集計に用いたい販売情報（Sale）のリスト
        :type sales: list
        """
        self.sales = sales

    @property
    def total(self):
        """
        販売情報リストの売り上げ合計値を取得

        :returns: 販売情報リストの売り上げ合計値
        :rtype: int
        """
        return sum([sale.total for sale in self.sales])

    @property
    def details(self):
        """
        販売情報リストの内訳を以下のようにカンマ区切りで取得。\n
        'ブルーベリー: 3000円(10), レモン: 1600円(20)
        , パイナップル: 2500円(10)'

        :returns: 販売情報リストの内訳
        :rtype: str
        """
        details_list = [self.__detail(sale) for sale in self.sales]
        return ', '.join(details_list)

    def __detail(self, sale):
        """
        販売情報の内訳を以下のようなフォーマットで取得\n
        'ブルーベリー: 3000円(10)'

        :param sale: 販売情報
        :type sale: Sale
        :returns: 販売情報の内訳
        :rtype: str
        """
        message = '{0}: {1}円({2})'
        return message.format(sale.fruit.name, sale.total, sale.number)
