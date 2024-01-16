# Generated by Django 4.2.7 on 2024-01-06 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_rename_product_offer_product_offer_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='offer_price',
            new_name='discounted_price',
        ),
        migrations.AddField(
            model_name='product',
            name='offer',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]