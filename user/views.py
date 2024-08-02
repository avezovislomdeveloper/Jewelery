from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from app.models import NavbarIcons
from . forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile
from app.models import Product
from django.contrib.auth import authenticate, login, logout
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .forms import LoginForm
from django.contrib import messages
from .forms import ReelsCreateForm
from . models import Reels
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')  
    logo = NavbarIcons.objects.all()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user=  authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html',{'form':form,'logo':logo})

def signin(request):
    if request.user.is_authenticated:
        return redirect('/')  
    logo = NavbarIcons.objects.all()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request,user)
                messages.info(request, f'You are now successfully loged in as {username}')
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html',{'logo':logo,'form':form})

def signout(request):
    logo = NavbarIcons.objects.all()
    logout(request)
    messages.info(request, 'You are successfully logged out ')
    return redirect('login')
  



class UserProfileView(ListView):
    model = Product
    template_name = 'user/profile.html'
    context_object_name = 'products'
    def get_queryset(self):
        self.user_profile = get_object_or_404(User, username=self.kwargs.get('username'))
        return Product.objects.filter(author=self.user_profile)
    
      
    def  get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        reels = Reels.objects.filter(reels=self.request.user)
        
     
            
        context['reels'] = reels
        context['user_profile'] = self.user_profile
        context['profile'] = get_object_or_404(Profile, user=self.user_profile)
        return context
    

def profile_update_form(request):
    logo = NavbarIcons.objects.all()
    profile = Profile.objects.get(user=request.user)
    user = request.user
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid() :
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile updated successfully')
            return redirect('/user/'+str(user))
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile_update_form.html',{'u_form':u_form,'p_form':p_form,'profile':profile,'logo':logo})




def reels_create(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)
    logo = NavbarIcons.objects.all()
    favourite_count = request.user.favourite.count()
    if request.method == "POST":
        form = ReelsCreateForm(request.POST, request.FILES)
        if form.is_valid():
            reel = form.save(commit=False)
            reel.user = user
            reel.save()
            return redirect('/user/'+str(user))
        
    else:
        form = ReelsCreateForm()
    return render(request, 'users/reels_create.html',{'profile':profile,'logo':logo,'favourite_count':favourite_count,'form':form})


@csrf_exempt
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('reelid'))
        reels_like = get_object_or_404(Reels, id=id)
        if reels_like.like.filter(id=request.user.id).exists():
            reels_like.like.remove(request.user)
            reels_like.like_count -= 1
            result = reels_like.like_count
            reels_like.save()
        
        else:
            reels_like.like.add(request.user)
            reels_like.like_count += 1
            result = reels_like.like_count
            reels_like.save()
            
        return JsonResponse({'result':result})