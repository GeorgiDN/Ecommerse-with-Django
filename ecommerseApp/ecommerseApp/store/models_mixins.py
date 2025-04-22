from django.db import models


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
