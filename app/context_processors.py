from django.conf import settings

def user_profile(request):
    if request.user.is_authenticated:
        try:
            return {'user_profile': request.user.profile.image.url}
        
        except:
            return {'user_profile': settings.MEDIA_URL + 'media_another/default.png'}
        
    return {}