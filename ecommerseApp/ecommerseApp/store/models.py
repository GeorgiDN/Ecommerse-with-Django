from django.core.validators import MinLengthValidator
from django.db import models
from PIL import Image

from ecommerseApp.accounts.models import Customer
from ecommerseApp.common.custom_validators import validate_phone_number


class Category(models.Model):
    name = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(
        max_length=100,
    )
    price = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=10
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category_products',
    )
    description = models.CharField(
        max_length=1500,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to='product_images',
        blank=True,
        null=True,
    )
    is_on_sale = models.BooleanField(
        default=False,
    )
    sale_price = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True
    )

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    def __str__(self):
        return f'Product {self.name}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customer_order',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
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
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'Order {self.id} - {self.customer}'

    def save(self, *args, **kwargs):
        if self.customer:
            self.phone = self.phone or self.customer.phone
            self.email = self.email or self.customer.email
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='order_items',
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='product_items',
    )
    quantity = models.PositiveIntegerField(
        default=1,
    )
    price_at_time_of_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.product.is_on_sale:
            self.price_at_time_of_order = self.product.price * self.quantity
        else:
            self.price_at_time_of_order = self.product.sale_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
