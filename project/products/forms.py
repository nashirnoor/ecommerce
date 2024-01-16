from django import forms
from .models import Product,ProductImage


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['product_name', 'description', 'category', 'stock', 'price', 'image','discount_price']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']