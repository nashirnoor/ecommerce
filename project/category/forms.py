# forms.py (create a new file if not existing)
from django import forms
from .models import Category
from django.core.exceptions import ValidationError


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description', 'image', 'category_offer_description', 'category_offer']

    def clean_category_name(self):
           # Check if a category with the same name already exists
        category_name = self.cleaned_data['category_name']
        # Check for whitespace-only values
        if category_name.strip() == '':
            raise ValidationError('Category name cannot be whitespace-only.')
        if Category.objects.filter(category_name=category_name).exists():
            raise ValidationError('Category with this name already exists.')
        return category_name
    
    def clean_category_offer(self):
        category_offer = self.cleaned_data['category_offer']

        # Check if the category_offer is below 99 and not negative
        if category_offer < 0:
            raise ValidationError('Category offer cannot be a negative value.')

        if category_offer >= 99:
            raise ValidationError('Category offer must be below 99.')

        return category_offer
    


 