from django.contrib import admin
from .models import NavbarIcons, Product, ProductImage, ProductUserPhoneNumber, Comment
# Register your models here.

admin.site.register(NavbarIcons)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductUserPhoneNumber)
admin.site.register(Comment)

