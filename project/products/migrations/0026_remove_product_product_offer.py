# Generated by Django 4.2.7 on 2024-01-05 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_alter_product_discounted_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_offer',
        ),
    ]