# Generated by Django 4.2.7 on 2023-12-23 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_remove_product_offer_product_discounted_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
