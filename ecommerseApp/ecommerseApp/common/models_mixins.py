from django.core.validators import MinLengthValidator
from django.db import models

from ecommerseApp.common.custom_validators import validate_phone_number, validate_lettres


class FirstNameMixin(models.Model):
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

    class Meta:
        abstract = True


class LastNameMixin(models.Model):
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

    class Meta:
        abstract = True


class EmailMixin(models.Model):
    email = models.EmailField(
        unique=True,
    )

    class Meta:
        abstract = True


class PhoneMixin(models.Model):
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

    class Meta:
        abstract = True


class QuantityMixin(models.Model):
    quantity = models.PositiveIntegerField(
        default=1,
    )

    class Meta:
        abstract = True


class PriceMixin(models.Model):
    price = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=10
    )

    class Meta:
        abstract = True
