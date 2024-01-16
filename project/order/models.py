from django.db import models
# from datetime import date
# from user.models import Customer,Address
# from products.models import Product,Coupon

# # Create your models here.
# class Order(models.Model):
#     ORDER_STATUS = (
#         ("pending", "Pending"),
#         ("processing", "processing"),
#         ("shipped", "shipped"),
#         ("delivered", "delivered"),
#         ("completed", "Completed"),
#         ("cancelled", "Cancelled"),
#         ("refunded", "refunded"),
#         ("on_hold", "on_hold"),
#     )

#     user = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     address = models.ForeignKey(Address, on_delete=models.CASCADE)
#     product = models.ForeignKey(
#         Product, on_delete=models.CASCADE, null=True, blank=True
#     )

#     amount = models.CharField(max_length=100)
#     payment_type = models.CharField(max_length=100)
#     status = models.CharField(max_length=100, choices=ORDER_STATUS, default="pending")
#     quantity = models.IntegerField(default=0, null=True, blank=True)
#     image = models.ImageField(upload_to="products", null=True, blank=True)
#     date = models.DateField(default=date.today)
#     coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return f"Order #{self.pk} - {self.product}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     image = models.ImageField(upload_to="products", null=True, blank=True)

#     def __str__(self):
#         return str(self.id)
