from datetime import date

from django.db import models


class FruitManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Fruit(models.Model):
    name = models.CharField('名称', unique=True, max_length=30)
    price = models.PositiveIntegerField('単価')
    reg_date = models.DateField('登録日時', default=date.today)

    objects = FruitManager()

    def __str__(self):
        return self.name
