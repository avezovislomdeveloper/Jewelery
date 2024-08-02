from django.urls import path
from . import views
from .views import UserProfileView

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('create_product', views.create_product, name='create-product'),
    path('favourites-list/', views.favourites_list, name='favourites_list'),
    path('fav/<int:pk>/', views.favourites_add, name='favourites_add'),
    path('product/<int:product_id>/', views.product_detail, name='product-detail'),
    path('product/<int:product_id>/comment', views.product_comment, name='product_comment'),
    path('confirm/<int:product_id>/', views.delete_product, name='delete_product'),
    path('update/<int:product_id>/', views.update_profile, name='update_profile'),
    
]
