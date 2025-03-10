from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shipping_addresses',
        null=True,
        blank=True,
    )
    full_name = models.CharField(
        max_length=255,
    )
    email = models.CharField(
        max_length=255,
    )
    address1 = models.CharField(
        max_length=255,
    )
    address2 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    state = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    zip = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    city = models.CharField(
        max_length=255,
    )
    country = models.CharField(
        max_length=255,
    )

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f'Shipping address {str(self.id)}'
