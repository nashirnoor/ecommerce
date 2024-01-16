from django.contrib import admin
from django.urls import path
from user import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user'

urlpatterns = [
    path('filter_sales/', views.filter_sales, name='filter_sales'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('adminn/', views.admin_login,name='admin'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('signup/', views.signupPage, name='signup'),
    path('otp/', views.verify_signup, name='otp'),
    path('customer/<int:customer_id>/block/', views.block_customer, name='block_customer'),
    path('customer/<int:customer_id>/unblock/', views.unblock_customer, name='unblock_customer'),
    path('Customer/',views.customers,name='customer'),
    path('',views.home,name='home'),
    path('logout/',views.logoutPage,name='logout'),
    path('verify_otp/',views.verify_signup,name='verify_signup'),
    path('profile/',views.profile,name='profile'),
    path('address/',views.address,name='address'),
    path('add_address/',views.add_address,name='add_address'),
    path('update_address/<int:id>',views.update_address,name='update_address'),
    path('delete_address/<int:id>/',views.delete_address,name='delete_address'),
    path('change_password/', views.change_password, name='change_password'),
    path('report-pdf-order/', views.report_pdf_order, name='report_pdf_order'),
    path('searchuser/',views.searchuser,name='searchuser'),


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
