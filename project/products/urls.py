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
from django.urls import path
from products import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('aaaa/',views.arr),
        path('apply_coupon/', views.apply_coupon, name='apply_coupon'),

    path('products/',views.product,name='products'),
    path('edit/<int:product_id>/',views.editproduct,name='edit_product'),
    path('product/<int:id>/update/', views.update, name='update'),
    path('add/', views.add_product, name='add_product'),
    path('userproduct/',views.userproductpage,name='userproduct'),
    path('single_product/<int:id>/',views.single_product,name='single_product'),
    path('cart/',views.cart,name='cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('coupon/',views.coupon,name = 'coupon'),
    path('addcoupon/',views.addcoupon,name='addcoupon'),
    # path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('wishlist/',views.wishlist, name='wishlist'),
    path('addtowishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:wishlist_item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('checkout',views.checkout,name='checkout'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('order/',views.order,name = 'order'),
    path('customerorder/',views.customer_order,name = 'customer_order'),
    path('success/',views.success,name='success'),
    path('cancel_success/',views.cancel_success,name='cancel_success'),
    path('update_order/', views.updateorder, name='update_order'),
    path('cancel-order/<int:order_id>/<int:order_item_id>/', views.cancel_order, name='cancel_order'),
    path('return-order/<int:order_id>/<int:order_item_id>/', views.return_order, name='return_order'),
    path('razorpay/<int:address_id>/',views.razorpay,name='razorpay'),
    path('wallet/',views.wallet,name='wallet'),
    path('order_details/<int:id>',views.order_details,name='order_details'),
    path('generate_invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
    path('<int:order_id>/download/', views.download_invoice, name='download_invoice'),
    path('search/',views.search,name='search'),
    path('searchproduct/',views.searchproduct,name='searchproduct'),
    path('display_brands/', views.display_brands, name='display_brands'),
    path('add_brand/', views.add_brand, name='add_brand'),
    path('display_brands/', views.display_brands, name='display_brands'),
    path('delete_brand/<int:brand_id>/', views.delete_brand, name='delete_brand'),



    




    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
