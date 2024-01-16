"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views
from products.views import update_cart,razorpay
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from products.views import proceedtopay
from products.views import cancel_order
from user.views import filter_sales

urlpatterns = [
    # path('bbb/',views.bbb),
    # path('asdf/',views.asdf,name='asdf'),
    # Other URL patterns...
  
    path('admin/', admin.site.urls),
    path('filter_sales/', filter_sales, name='filter_sales'),
    path('products/',include('products.urls')),
    path('category/',include('category.urls')),
    path('banner/',include('banner.urls')),   
    path('user/', include('user.urls', namespace='user')), 
    path('cart/', include('cart.urls', namespace='cart')),
    path('update-cart/<int:product_id>/', update_cart, name='update_cart'),
    path('adminn/', views.admin_login,name='admin'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('signup/', views.signupPage, name='signup'),
    path('otp/', views.verify_signup, name='otp'),   
    path('customer/<int:customer_id>/block/', views.block_customer, name='block_customer'),
    path('customer/<int:customer_id>/unblock/', views.unblock_customer, name='unblock_customer'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('Customer/',views.customers,name='customer'),
    path('',views.home,name='home'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('login', views.loginPage, name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('verify_otp/',views.verify_signup,name='verify_signup'),
    path('proceed-to-pay',proceedtopay,name='proceedtopay'),
    path('razorpay/<int:address_id>/',razorpay,name='razorpay'),



]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
