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


class ProductEditForm(ProductBaseForm):
    pass


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


# class CategoryEditForm(CategoryBaseForm):
#     pass


class CategoryEditForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['products'].initial = self.instance.category_products.all()

    def save(self, commit=True):
        category = super().save(commit=False)
        if commit:
            category.save()
        category.category_products.set(self.cleaned_data['products'])
        self.save_m2m()
        return category
