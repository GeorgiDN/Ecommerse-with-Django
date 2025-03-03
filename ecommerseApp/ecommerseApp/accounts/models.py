from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

from ecommerseApp import settings
from ecommerseApp.common.custom_validators import validate_lettres, validate_phone_number


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Customer(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile',
    )
    first_name = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(
                1,
                message='The length of the name must be between 1 and 50 characters.'),
            validate_lettres
        ],
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(
                1,
                message='The length of the name must be between 1 and 50 characters.'),
            validate_lettres
        ],
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(
                4,
                message='Phone number must be between 4 and 20 digits.'),
            validate_phone_number],
        null=True,
        blank=True,
    )
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
