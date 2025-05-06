from django.db import models


class DescribedModel(models.Model):
    url_slug = models.SlugField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1500, blank=True, null=True)
    meta_title = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.CharField(max_length=1500, blank=True, null=True)

    class Meta:
        abstract = True


class BaseProductMixin(models.Model):
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True, help_text="Stock Keeping Unit (unique)")
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=10, null=True, blank=True)
    track_quantity = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    weight = models.DecimalField(default=0, decimal_places=3, max_digits=12, null=True, blank=True)

    class Meta:
        abstract = True


class UrlMixin(models.Model):
    url_slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.CharField(
        max_length=200,
    )

    class Meta:
        abstract = True


class DescriptionMixin(models.Model):
    description = models.CharField(
        max_length=1500,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class MetaTitleMixin(models.Model):
    meta_title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class MetaDescriptionMixin(models.Model):
    meta_description = models.CharField(
        max_length=1500,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class IsActiveMixin(models.Model):
    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        abstract = True
