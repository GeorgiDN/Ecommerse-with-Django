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
    shipping_full_name = models.CharField(
        max_length=255,
        help_text='First and last name',
        null=True,
        blank=True,
    )
    shipping_email = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    shipping_address1 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
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
        null=True,
        blank=True,
    )
    shipping_country = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f'Shipping address {str(self.id)}'
