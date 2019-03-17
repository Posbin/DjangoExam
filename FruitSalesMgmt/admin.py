from django.contrib import admin

from .models import Fruit, Sale


class FruitAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'reg_date')


class SaleAdmin(admin.ModelAdmin):
    list_display = ('fruit', 'number', 'total', 'datetime')


admin.site.register(Fruit, FruitAdmin)
admin.site.register(Sale, SaleAdmin)
