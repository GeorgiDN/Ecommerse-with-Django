from django.forms import ModelForm
from django import forms
from ecommerseApp.store.models import Product, Category


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


class ProductEditForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': 10
        })
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'is_on_sale', 'sale_price', 'sku', 'model',
                  'is_active', 'is_available', 'quantity', 'track_quantity', 'weight', 'categories',
                  'url_slug', 'meta_title', 'meta_description',
                  ]

        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
                'cols': 60,
                'class': 'form-control',
                'placeholder': 'Enter product description here...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['categories'].initial = self.instance.categories.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
            instance.categories.set(self.cleaned_data['categories'])
        return instance


class CategoryBaseForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
                'cols': 60,
                'class': 'form-control',
                'placeholder': 'Enter category description here...'
            }),
        }


class CategoryCreateForm(CategoryBaseForm):
    pass



class CategoryEditForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': 10
        })
    )

    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'products']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
                'cols': 60,
                'class': 'form-control',
                'placeholder': 'Enter category description here...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['products'].initial = self.instance.category_products.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
            instance.category_products.set(self.cleaned_data['products'])
        return instance
