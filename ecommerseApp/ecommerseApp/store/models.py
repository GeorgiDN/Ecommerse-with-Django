from django.core.validators import MinLengthValidator
from django.db import models
from PIL import Image
from django.utils.text import slugify

from ecommerseApp.accounts.models import Profile
from ecommerseApp.common.models_mixins import FirstNameMixin, LastNameMixin, PhoneMixin, EmailMixin, QuantityMixin, \
    PriceMixin
from ecommerseApp.store.models_mixins import UrlMixin, NameMixin, DescriptionMixin, MetaTitleMixin, \
    MetaDescriptionMixin, IsActiveMixin, DescribedModel, BaseProductMixin


class Category(DescribedModel, IsActiveMixin, models.Model):
    image = models.ImageField(upload_to='category_images', blank=True, null=True, default='default.png')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.url_slug:
            self.url_slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = self.name
        if not self.meta_description:
            self.meta_description = self.description
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'


class Customer(FirstNameMixin, LastNameMixin, PhoneMixin, EmailMixin, models.Model):
    password = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(DescribedModel, BaseProductMixin, IsActiveMixin, models.Model):
    image = models.ImageField(upload_to='product_images', blank=True, null=True, default='default.png')
    categories = models.ManyToManyField(Category, related_name='category_products', blank=True)
    model = models.CharField(max_length=100, blank=True, null=True, help_text="Model number or reference")
    tags = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    def save(self, *args, **kwargs):
        if not self.url_slug:
            self.url_slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = self.name
        if not self.meta_description:
            self.meta_description = self.description
        super().save(*args, **kwargs)


class ProductOption(models.Model):
    product = models.ForeignKey( Product, related_name='product_options', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class ProductOptionValue(models.Model):
    option = models.ForeignKey(ProductOption, related_name='option_values', on_delete=models.CASCADE)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.option.name}: {self.value}"


class ProductVariant(BaseProductMixin, models.Model):
    product = models.ForeignKey(Product, related_name='product_variants', on_delete=models.CASCADE)
    option_values = models.ManyToManyField(ProductOptionValue, related_name='variants')

    def __str__(self):
        values = ", ".join([v.value for v in self.option_values.all()])
        return f"{self.product.name} Variant - {values or self.sku}"


class Order(PhoneMixin, QuantityMixin, models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    product = models.ForeignKey(
        to=Product,
        on_delete=models.SET_NULL,
        related_name='product_orders',
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='customer_order',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    address = models.CharField(max_length=200)

    def __str__(self):
        return f'Order {self.id} - {self.customer}'

    # def save(self, *args, **kwargs):
    #     if self.customer:
    #         self.phone = self.phone or self.customer.phone
    #         self.email = self.email or self.customer.email
    #     super().save(*args, **kwargs)
