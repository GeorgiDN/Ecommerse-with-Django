import re

from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not re.match(r'^\d+$', value):
        raise ValidationError('Phone number should contain only numbers!')


def validate_lettres(value):
    if not re.match(r'^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ]+$', value):
        raise ValidationError('Name should contain only letters!')
