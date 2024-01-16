from django.db import models




class Banner(models.Model):
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    description = models.CharField(max_length=100)
    offer_description = models.CharField(max_length=100)
