# Generated by Django 5.0.1 on 2024-01-15 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_customer_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='wallet_bal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]
