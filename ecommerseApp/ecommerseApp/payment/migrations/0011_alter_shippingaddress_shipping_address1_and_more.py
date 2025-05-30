# Generated by Django 5.1.6 on 2025-03-12 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_address1',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_email',
            field=models.EmailField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_full_name',
            field=models.CharField(default=1, help_text='First and last name', max_length=255),
            preserve_default=False,
        ),
    ]
