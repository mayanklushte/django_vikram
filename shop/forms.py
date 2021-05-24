from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'
        exclude = ('user',)
        widgets = {
            'Product_Name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product Name',                
            }),
            'Description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description'
            }),
            'Quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                
            }),
            'Brand_Name': forms.TextInput(attrs={
                'class': 'form-control ',
                'placeholder': 'Brand Name'
            }),
            'Price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': ''
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': ''
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category'
            }),
        }
        