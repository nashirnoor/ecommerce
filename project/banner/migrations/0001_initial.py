# Generated by Django 4.2.7 on 2024-01-10 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('description', models.CharField(max_length=100)),
                ('offer_description', models.CharField(max_length=100)),
            ],
        ),
    ]
