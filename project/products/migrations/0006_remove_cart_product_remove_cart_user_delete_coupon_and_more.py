# Generated by Django 4.2.7 on 2023-12-13 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
        migrations.DeleteModel(
            name='Coupon',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='product',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='user',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
