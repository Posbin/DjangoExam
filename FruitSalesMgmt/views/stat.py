from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from ..models import Sale


@login_required
def stats(request):
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
    stats = {}
    this_month = timezone.now().date().replace(day=1)
    dates = [this_month - relativedelta(months=ago) for ago in range(num)]
    for date in dates:
        key = '{:%Y/%m}'.format(date)
        sales = list(filter(same_month_filter(date), all_sales))
        stats[key] = Stat(sales)
    return stats


def get_daily_stats(all_sales, num):
    stats = {}
    today = timezone.now().date()
    dates = [today - timedelta(days=ago) for ago in range(num)]
    for date in dates:
        key = '{:%Y/%m/%d}'.format(date)
        sales = list(filter(same_day_filter(date), all_sales))
        stats[key] = Stat(sales)
    return stats


def same_month_filter(date):
    return lambda s: s.datetime.date().replace(day=1) == date


def same_day_filter(date):
    return lambda s: s.datetime.date() == date


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
        message = '{0}: {1}円({2})'
        return message.format(sale.fruit.name, sale.total, sale.number)
