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

class ProductOptionValueForm(forms.ModelForm):
    class Meta:
        model = ProductOptionValue
        fields = ['value']
        widgets = {
            'value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Red, Large'
            })
        }

class ProductOptionForm(forms.ModelForm):
    class Meta:
        model = ProductOption
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Color, Size'
            })
        }

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['sku', 'price', 'is_on_sale', 'sale_price', 'quantity', 'weight', 'option_values']
        widgets = {
            'option_values': forms.SelectMultiple(attrs={
                'class': 'form-control select2-multiple',
                'multiple': 'multiple'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'sale_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
        }

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if product:
            # Filter option values based on the product's options
            self.fields['option_values'].queryset = ProductOptionValue.objects.filter(
                option__product=product
            )

# Formsets
ProductOptionFormSet = inlineformset_factory(
    Product, ProductOption,
    form=ProductOptionForm,
    extra=1,
    can_delete=True
)

ProductVariantFormSet = inlineformset_factory(
    Product, ProductVariant,
    form=ProductVariantForm,
    extra=1,
    can_delete=True,
    fk_name='product'
)

# #############################


class ProductOptionValueFormm(forms.ModelForm):
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
    class Meta:
        model = ProductOption
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Color, Size'
            })
        }

# Create a base formset that includes option values
class BaseProductOptionFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize option value formsets for existing options
        for form in self.forms:
            if form.instance.pk:
                form.option_value_formset = ProductOptionValueFormSet(
                    instance=form.instance,
                    prefix=f'option_{form.instance.pk}_values'
                )

ProductOptionValueFormSet = inlineformset_factory(
    ProductOption, ProductOptionValue,
    form=ProductOptionValueFormm,
    extra=1,
    can_delete=True
)

ProductOptionFormSett = inlineformset_factory(
    Product, ProductOption,
    form=ProductOptionForm,
    formset=BaseProductOptionFormSet,
    extra=1,
    can_delete=True
)




# ProductOptionFormSet = inlineformset_factory(
#     Product, ProductOption,
#     form=ProductOptionForm,
#     formset=BaseProductOptionFormSet,
#     extra=1,
#     can_delete=True
# )
#
#
# ProductOptionValueFormSet = inlineformset_factory(
#     ProductOption, ProductOptionValue,
#     form=ProductOptionValueForm,
#     extra=1,
#     can_delete=True
# )
#
# ProductVariantFormSet = inlineformset_factory(
#     Product, ProductVariant,
#     form=ProductVariantForm,
#     extra=1,
#     can_delete=True
# )




# class ProductOptionForm(forms.ModelForm):
#     class Meta:
#         model = ProductOption
#         fields = ['name']
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'e.g., Color, Size'
#             })
#         }
#
# class ProductOptionValueForm(forms.ModelForm):
#     class Meta:
#         model = ProductOptionValue
#         fields = ['value']
#         widgets = {
#             'value': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'e.g., Red, Large'
#             })
#         }
#
# class ProductVariantForm(forms.ModelForm):
#     class Meta:
#         model = ProductVariant
#         fields = ['sku', 'price', 'is_on_sale', 'sale_price', 'track_quantity', 'quantity', 'weight', 'option_values']
#         widgets = {
#             'option_values': forms.SelectMultiple(attrs={
#                 'class': 'form-control select2',
#             }),
#             'price': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'step': '0.01'
#             }),
#             'sale_price': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'step': '0.01'
#             }),
#         }
#
# # Create formsets
# ProductOptionFormSet = inlineformset_factory(
#     Product, ProductOption,
#     form=ProductOptionForm,
#     extra=1,
#     can_delete=True
# )
#
# ProductOptionValueFormSet = inlineformset_factory(
#     ProductOption, ProductOptionValue,
#     form=ProductOptionValueForm,
#     extra=1,
#     can_delete=True
# )
#
# ProductVariantFormSet = inlineformset_factory(
#     Product, ProductVariant,
#     form=ProductVariantForm,
#     extra=1,
#     can_delete=True
# )
