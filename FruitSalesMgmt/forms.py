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

class SalesDataUploadForm(forms.Form):
    file = forms.FileField(
        label='',
        widget=forms.FileInput(attrs={'accept':'text/csv'})
    )
