from django.db import models
import datetime

class FruitManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Fruit(models.Model):
    name = models.CharField('名称', unique = True, max_length = 30)
    price = models.PositiveIntegerField('単価')
    reg_date = models.DateField(default = datetime.date.today)

    objects = FruitManager()

    def __str__(self):
        return self.name

class Sale(models.Model):
    fruit = models.ForeignKey('Fruit', on_delete = models.CASCADE, verbose_name='果物')
    number = models.PositiveIntegerField('個数')
    total = models.PositiveIntegerField()
    datetime = models.DateTimeField('販売日時')

    def __str__(self):
        return "{0} {1} × {2}".format(
            self.datetime.date(),
            self.fruit.name,
            self.number
        )
