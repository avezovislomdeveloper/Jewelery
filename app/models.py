from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField 
from django_countries.fields import CountryField

# Create your models here.

class NavbarIcons(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media_another/')
    
    def __str__(self):
        return self.name
    
    

class Product(models.Model):
    options = (
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    option = models.CharField(max_length=10, choices=options, default='gold')
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    
    def __str__(self):
        return self.name

class ProductUserPhoneNumber(models.Model):
    product = models.OneToOneField(Product, related_name='phone_number', on_delete=models.CASCADE)
    number = PhoneNumberField()
    country = CountryField()

    def __str__(self):
        return self.product.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media_another/')
    
    
    def __str__(self):
        return f"Image for {self.product.name}"
    


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.name
    
    