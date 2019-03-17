from django.db import models

class Sale(models.Model):
    fruit = models.ForeignKey('Fruit', on_delete=models.CASCADE, verbose_name='果物')
    number = models.PositiveIntegerField('個数')
    total = models.PositiveIntegerField('売り上げ')
    datetime = models.DateTimeField('販売日時')

    def __str__(self):
        return "{0} {1} × {2}".format(
            self.datetime.date(),
            self.fruit.name,
            self.number
        )
