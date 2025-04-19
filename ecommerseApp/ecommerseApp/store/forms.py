from django.forms import ModelForm

from ecommerseApp.store.models import Product


class ProductEditForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
