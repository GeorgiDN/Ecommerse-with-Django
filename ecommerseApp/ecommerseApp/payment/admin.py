from django.contrib import admin

from ecommerseApp.payment.models import ShippingAddress

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    pass
