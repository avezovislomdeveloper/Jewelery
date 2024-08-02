from django import forms
from .models import Product, ProductImage, ProductUserPhoneNumber, Comment

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'option']


class ProductUserPhoneNumberForm(forms.ModelForm):
    class Meta:
        model = ProductUserPhoneNumber
        fields = ['number']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']