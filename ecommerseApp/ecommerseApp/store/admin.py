from django.contrib import admin
from ecommerseApp.store.models import Category, Product, Order, ProductOption, ProductOptionValue, ProductVariant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


class ProductOptionValueInline(admin.TabularInline):
    model = ProductOptionValue
    extra = 1


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    filter_horizontal = ['option_values']
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductOptionInline, ProductVariantInline]


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    inlines = [ProductOptionValueInline]


admin.site.register(ProductVariant)
