# Generated by Django 4.2.7 on 2024-01-04 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_alter_order_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_offer',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4),
        ),
    ]
