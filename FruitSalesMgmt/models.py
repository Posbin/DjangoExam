from django.db import models
import datetime

class FruitManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Fruit(models.Model):
    name = models.CharField(unique = True, max_length = 30)
    price = models.PositiveIntegerField()
    reg_date = models.DateField(default = datetime.date.today)

    objects = FruitManager()

class Sale(models.Model):
    fruit = models.ForeignKey('Fruit', on_delete = models.CASCADE)
    number = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    datetime = models.DateTimeField()
