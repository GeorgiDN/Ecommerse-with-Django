from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from ecommerseApp import settings
from ecommerseApp.common.models_mixins import FirstNameMixin, LastNameMixin, PhoneMixin


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Profile(FirstNameMixin, LastNameMixin, PhoneMixin,  models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile',
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
    old_cart = models.CharField(
        max_length=1500,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
