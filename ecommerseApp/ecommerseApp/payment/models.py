from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model

from ecommerseApp.common.custom_validators import validate_phone_number
from ecommerseApp.common.models_mixins import EmailMixin, QuantityMixin, PriceMixin, PhoneMixin
from ecommerseApp.store.models import Product, ProductVariant

User = get_user_model()


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shipping_addresses',
        null=True,
        blank=True,
    )
    shipping_full_name = models.CharField(
        max_length=255,
        help_text='First and last name',
    )
    shipping_email = models.CharField(
        max_length=255,
    )
    shipping_phone = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(
                4,
                message='Phone number must be between 4 and 20 digits.'),
            validate_phone_number],
    )
    shipping_address1 = models.CharField(
        max_length=255,
    )
    shipping_address2 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    shipping_state = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    shipping_zip = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    shipping_city = models.CharField(
        max_length=255,
    )
    shipping_country = models.CharField(
        max_length=255,
    )

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f'Shipping address {str(self.id)}'


class Order(PhoneMixin, models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_orders',
        null=True,
        blank=True,
    )
    full_name = models.CharField(
        max_length=255,
        help_text='First and last name',
        null=True,
        blank=True,
    )
    email = models.CharField(
        max_length=255,
    )
    shipping_address = models.TextField(
        max_length=15000,
    )
    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    date_ordered = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )
    shipped = models.BooleanField(
        default=False,
    )
    date_shipped = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('date_ordered',)

    def __str__(self):
        return f'Order - #{str(self.id)}'


class OrderItem(QuantityMixin, PriceMixin, models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='product_items',
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_items',
        null=True,
        blank=True,
    )
    quantity = models.PositiveBigIntegerField(
        default=1,
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    variant = models.ForeignKey(
        to=ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='variant_items'
    )

    option_details = models.JSONField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Order Item - #{self.id}'
