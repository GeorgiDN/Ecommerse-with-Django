# Generated by Django 5.1.6 on 2025-04-27 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_productvariant_is_on_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='track_quantity',
            field=models.BooleanField(default=True),
        ),
    ]
