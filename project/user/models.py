from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone
# from products.models import Order
# Create your models here.

class Customer(AbstractUser):
    username           =   models.CharField(unique=True,null=True,blank=True,max_length=20)
    email              =   models.EmailField(unique=True)
    number             =   models.CharField(max_length=10)
    is_verified        =   models.BooleanField(default=False)
    email_token        =   models.CharField(max_length=100, null=True, blank=True)
    forgot_password    =   models.CharField(max_length=100,null=True, blank=True)
    last_login_time    =   models.DateTimeField(null = True, blank = True)
    last_logout_time   =   models.DateTimeField(null=True,blank=True)
    profile_photo      =   models.ImageField(upload_to='products', null=True, blank=True)
    referral_code      =   models.CharField(max_length=100,null=True, unique=True)
    referral_amount    =   models.IntegerField(default=0)
    date_joined = models.DateTimeField(default=timezone.now)  # New field for registration date

    wallet_bal         =   models.DecimalField(max_digits=100, decimal_places=2, default=0.00)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.email
    
class Address(models.Model):
    user              = models.ForeignKey(Customer,on_delete=models.CASCADE)
    address_name      = models.CharField(max_length=50, null=False, blank=True)
    first_name        = models.CharField(max_length=50, null=False, blank=True)
    last_name         = models.CharField(max_length=50, null=False,blank=True)
    email             = models.EmailField()
    address_1         = models.CharField(max_length=250, blank=True)
    address_2         = models.CharField(max_length=250, blank=True)
    country           = models.CharField(max_length=15)
    state             = models.CharField(max_length=15)
    city              = models.CharField(max_length=15)
    pin               = models.IntegerField()
    is_deleted        = models.BooleanField(default=False)
    default           = models.BooleanField(default=False)
    objects = models.Manager()
    def __str__(self):
        return f"{self.address_name} "
    



    












class Slider(models.Model):
    DISCOUNT_DEAL = (
        ('HOT DEALS', 'HOT DEALS'),
        ('New Arrivals', 'New Arrivals'),
    )

    Image = models.ImageField(upload_to='media/slider_imgs')
    Discount_Deal = models.CharField(choices=DISCOUNT_DEAL,max_length=100)
    SALE = models.IntegerField()
    
    Discount = models.IntegerField()
   

    