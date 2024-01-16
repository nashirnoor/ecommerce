# from django.db import models
# from products.models import Product
# from user.models import Customer

# # Create your models here.
# class Cart(models.Model):
#     user           =     models.ForeignKey(Customer, on_delete=models.CASCADE,null=True,blank=True)
#     product        =     models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
#     quantity       =     models.IntegerField(default=0)
#     image          =     models.ImageField(upload_to='products',null=True, blank=True )
#     device              = models.CharField(max_length=255, null=True, blank=True)

#     @property
#     def sub_total(self):
#         return self.product.price * self.quantity

#     def __str__(self):
#           return f"Cart: {self.user.username} - {self.product} - Quantity: {self.quantity}"
    
# class Coupon(models.Model):
#     coupon_code     =  models.CharField(max_length=100)
#     expired         =  models.BooleanField(default=False)
#     discount_price  =  models.PositiveIntegerField(default=100)
#     minimum_amount  =  models.PositiveIntegerField(default=500)
#     expiry_date     =  models.DateField(null=True,blank=True)

#     def __str__(self):
#         return self.coupon_code 
    

# class Wishlist(models.Model):
#     user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="products", null=True, blank=True)
#     device = models.CharField(max_length=255, null=True, blank=True)

#     def __str__(self):
#         return f"Wishlist:{self.user.username}-{self.product}"

    




