# Generated by Django 2.0.13 on 2019-03-04 10:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FruitSalesMgmt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fruit',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='fruit',
            name='price',
            field=models.PositiveIntegerField(verbose_name='単価'),
        ),
        migrations.AlterField(
            model_name='fruit',
            name='reg_date',
            field=models.DateField(default=datetime.date.today, verbose_name='登録日時'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='datetime',
            field=models.DateTimeField(verbose_name='販売日時'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='fruit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FruitSalesMgmt.Fruit', verbose_name='果物'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='number',
            field=models.PositiveIntegerField(verbose_name='個数'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total',
            field=models.PositiveIntegerField(verbose_name='売り上げ'),
        ),
    ]
