from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('update/', views.profile_update_form, name='update'),
    path('reels_upload/', views.reels_create, name='reel_create'),
    path('like/', views.like, name='like')
]