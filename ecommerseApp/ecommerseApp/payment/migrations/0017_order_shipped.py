# Generated by Django 5.1.6 on 2025-03-14 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0016_alter_orderitem_price_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]
