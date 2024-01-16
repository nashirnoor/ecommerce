from django.db import models

# Create your models here.

class Category(models.Model):
    category_name               =   models.CharField(max_length=100)
    description                 =   models.CharField(max_length=1000,default='')
    image                       =   models.ImageField(upload_to='products')
    category_offer_description  =   models.CharField(max_length=100, null=True, blank=True)
    category_offer              =   models.DecimalField(max_digits=4, decimal_places=1, default=0)
    is_listed = models.BooleanField(default=True)
    def __str__(self):
        return self.category_name
