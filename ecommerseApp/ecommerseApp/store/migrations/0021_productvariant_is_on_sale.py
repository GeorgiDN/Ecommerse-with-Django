# Generated by Django 5.1.6 on 2025-04-24 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_alter_productvariant_sku'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='is_on_sale',
            field=models.BooleanField(default=False),
        ),
    ]
