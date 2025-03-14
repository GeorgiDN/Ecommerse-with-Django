from django.contrib import admin

from ecommerseApp.payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth import get_user_model
User = get_user_model()


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    fields = ['user', 'full_name', 'email', 'shipping_address', 'amount_paid', 'date_ordered', 'shipped']
    inlines = [OrderItemInline]


admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)
