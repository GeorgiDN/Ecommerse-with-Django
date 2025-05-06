from django.forms import ModelForm, BaseInlineFormSet
from django import forms
from ecommerseApp.store.models import Product, Category, ProductOption, ProductOptionValue, ProductVariant
from django.forms import inlineformset_factory


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
        fields = ['name', 'description', 'image', 'price', 'is_on_sale', 'sale_price', 'sku', 'model', 'tags',
                  'is_active', 'is_available', 'quantity', 'track_quantity', 'weight', 'categories', 'has_options',
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


class ProductOptionValueForm(forms.ModelForm):
    class Meta:
        model = ProductOptionValue
        fields = ['value']
        widgets = {
            'value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter option value'
            })
        }


class ProductOptionForm(forms.ModelForm):
    values = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Comma-separated values (e.g., Red,Blue,Green)'
        }),
        help_text="Enter multiple values separated by commas"
    )

    class Meta:
        model = ProductOption
        fields = ['name', 'values']


class ProductOptionEditForm(forms.ModelForm):
    values = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'One value per line or comma-separated',
            'rows': 3
        }),
        help_text="Current values will be replaced. Separate with commas or new lines"
    )

    class Meta:
        model = ProductOption
        fields = ['name', 'values']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            existing_values = self.instance.option_values.all()
            self.initial['values'] = "\n".join([v.value for v in existing_values])


class ProductVariantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

        if product:
            # Only show option values that belong to this product
            self.fields['option_values'].queryset = ProductOptionValue.objects.filter(
                option__product=product
            )

    class Meta:
        model = ProductVariant
        fields = [
            'sku', 'price', 'is_on_sale', 'sale_price',
            'track_quantity', 'quantity', 'is_available',
            'weight', 'option_values'
        ]
        widgets = {
            'option_values': forms.SelectMultiple(attrs={
                'class': 'select2-multiple',
                'style': 'width: 100%'
            }),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'sale_price': forms.NumberInput(attrs={'step': '0.01'}),
            'weight': forms.NumberInput(attrs={'step': '0.01'}),
        }



class ProductVariantEditForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = [
            'sku', 'price', 'is_on_sale', 'sale_price',
            'track_quantity', 'quantity', 'is_available',
            'weight', 'option_values'
        ]
        widgets = {
            'option_values': forms.SelectMultiple(attrs={
                'class': 'select2-multiple',
                'style': 'width: 100%'
            }),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'sale_price': forms.NumberInput(attrs={'step': '0.01'}),
            'weight': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

        if product:
            self.fields['option_values'].queryset = \
                ProductOptionValue.objects.filter(option__product=product)


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
        fields = ['name', 'description', 'image', 'url_slug', 'meta_title', 'meta_description', 'products']
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

