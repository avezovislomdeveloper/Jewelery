from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField 
# Create your models here.


class Profile(models.Model):
    COUNTRY_CODES = (
        ('+998', '+998 (UZB)'),
        # Add more country codes as needed
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE )
    phone_number = PhoneNumberField()
    country_code = models.CharField(max_length=5, choices=COUNTRY_CODES, default='+998')
    experience = models.CharField(max_length=2)
    image = models.ImageField(default='media_another/default.png',upload_to='media_another/')
    
    def __str__(self):
        return self.user.username
    
    
    
class Reels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
    date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    
    def __str__(self):
        return self.name