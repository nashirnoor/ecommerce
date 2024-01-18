from django.contrib import admin
from django.urls import path
from category import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('category/',views.category, name = 'category'),
    path('addc/',views.add_category,name= 'add_category'),
    path('category/<int:id>/update_category/', views.update_category, name='update_category'),
    path('category/<int:category_id>/edit/', views.editcategory, name='edit_category'),
    path('category_products/<int:id>/', views.category_products, name='category_products'),
    path('usercategory/',views.usercategory,name='usercategory'),
    path('searchcategory/',views.searchcategory,name='searchcategory'),
    path('searchcategoryuser/',views.searchcategoryuser,name='searchcategoryuser')


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
