from django.db import models
from user.models import Customer,Address
from category.models import Category
from datetime import date
from decimal import Decimal

# Create your models here.

class Product(models.Model):   
    product_name   =     models.CharField(max_length=100)
    description    =     models.CharField(max_length=1000,default='') 
    category       =     models.ForeignKey(Category, on_delete=models.CASCADE)
    stock          =     models.IntegerField(default=0)
    price          =     models.IntegerField(default=0)
    image          =     models.ImageField(upload_to='products')
    # product_offer  =     models.PositiveBigIntegerField(default=0,null=True)
    offer = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_offer =   models.DecimalField(max_digits=4, decimal_places=1, default=0)
    is_deleted     =     models.BooleanField(default=False)
    is_listed = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):
        category_offer = Decimal(self.category.category_offer)
        product_offer = Decimal(self.product_offer)
        # Calculate the effective offer by comparing category and product offers
        effective_offer = max(category_offer,product_offer)
        self.offer = effective_offer
        # Calculate discounted price based on the effective offer
        self.discounted_price = Decimal(self.price) * (1 - effective_offer / 100)


        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return f"Image for {self.product.product_name}"
    


class Wishlist(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products", null=True, blank=True)
    device = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Wishlist:{self.user.username}-{self.product}"
    

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=100)
    expired = models.BooleanField(default=False)
    discount_price = models.PositiveIntegerField(default=100)
    minimum_amount = models.PositiveIntegerField(default=500)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.coupon_code

    
class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to="products", null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return (
            f"Cart: {self.user.username} - {self.product} - Quantity: {self.quantity}"
        )
    


class Order(models.Model):
    ORDER_STATUS = (
        ("pending", "Pending"),
        ("processing", "processing"),
        ("shipped", "shipped"),
        ("delivered", "delivered"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("refunded", "refunded"),
        ("on_hold", "on_hold"),
    )

    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='order_user')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='order_address')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True, related_name='order_product'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=ORDER_STATUS, default="pending")
    quantity = models.IntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to="products", null=True, blank=True)
    date = models.DateField(default=date.today)


    def __str__(self):
        return f"Order #{self.pk} - {self.product}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderitem_product')
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to="products", null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
class Wallet(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_credit = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20,blank=True)

    def _str_(self):
        return f"{self.amount} {self.is_credit}"

    def _iter_(self):
        yield self.pk



class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
