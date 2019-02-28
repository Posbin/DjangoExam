from django import forms
from .models import Fruit, Sale

class FruitForm(forms.ModelForm):

    class Meta:
        model = Fruit
        fields = ('name', 'price')

class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        fields = ('fruit', 'number', 'datetime')