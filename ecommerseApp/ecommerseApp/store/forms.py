from django.forms import ModelForm
from django import forms
from ecommerseApp.store.models import Product


class ProductBaseForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
                'cols': 60,
                'class': 'form-control',
                'placeholder': 'Enter product description here...'
            }),
        }


class ProductCreateForm(ProductBaseForm):
    pass


class ProductEditForm(ProductBaseForm):
    pass
