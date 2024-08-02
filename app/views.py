from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from .models import NavbarIcons
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from django.contrib.auth.models import User
from user.models import Profile
from . forms import ProductForm, CommentForm
from .models import ProductImage, Product, ProductUserPhoneNumber , Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from . forms import ProductUserPhoneNumberForm, ProductImageForm
from user.models import Reels
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

@login_required
def home(request):
    logo = NavbarIcons.objects.all()
    profile = Profile.objects.get(user=request.user)
    products = Product.objects.all().order_by('-id')
    
    favourite_count = Product.objects.filter(favourites=request.user).count()
    query = request.GET.get('query', '')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(option__icontains=query))[:1000]
        if not products:
            pass
        
        else:
            products = products[:1000]
    return render(request, 'core/index.html',{'logo':logo,'profile':profile,'products':products,'favourite_count':favourite_count,'query':query})

def base(request):  
    profile = Profile.objects.filter(user=request.user)
    
    profile = Profile.objects.get(user=request.user)
    favourite_count = Product.objects.filter(favourites=request.user).count()

    logo = NavbarIcons.objects.all()
    return render(request, 'core/base.html',{'logo':logo,'profile':profile,'favourite_count':favourite_count})



class UserProfileView(ListView):
    model = Product
    template_name = 'core/product_list_profile.html'
    context_object_name = 'products'
    def get_queryset(self):
        self.user_profile = get_object_or_404(User, username=self.kwargs.get('username'))
        return Product.objects.filter(author=self.user_profile).order_by('-id')
    
      
    def  get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        reels = Reels.objects.filter(user=self.user_profile)
        favourite_count = Product.objects.filter(favourites=self.request.user).count()
        
        logo = NavbarIcons.objects.all()
     
        context['reels'] = reels
        context['logo'] =logo 
        context['favourite_count'] = favourite_count
        context['user_profile'] = self.user_profile
        context['profile'] = get_object_or_404(Profile, user=self.user_profile)
        return context
    

def create_product(request):
    profile = Profile.objects.get(user=request.user)
    logo = NavbarIcons.objects.all()
    favourite_count = request.user.favourite.count()
    form_number = ProductUserPhoneNumberForm()
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        form_number = ProductUserPhoneNumberForm(request.POST)
        images = request.FILES.getlist('images')

        if product_form.is_valid() and form_number.is_valid():
            product = product_form.save(commit=False)
            product.author = request.user
            product.save()

            phone_number = form_number.save(commit=False)
            phone_number.product = product
            phone_number.save()
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            return redirect('home')  

    else:
        product_form = ProductForm()

    return render(request, 'core/create_product.html', {
        'product_form': product_form,
        'profile':profile,
        'logo':logo,
        'favourite_count':favourite_count,
        'form_number':form_number
    })
    

def favourites_list(request):
    if not request.user.is_authenticated:
        return redirect(reverse('myapp:signup'))
    favourite_count = Product.objects.filter(favourites=request.user).count()
    logo = NavbarIcons.objects.all()
    profile = Profile.objects.get(user=request.user)
    products = Product.objects.filter(favourites=request.user)
    return render(request, 'core/favourites_list.html',{'logo':logo,'profile':profile,'products':products,'favourite_count':favourite_count})



def favourites_add(request, pk):
    
    if request.method == "POST":
        product = get_object_or_404(Product, pk=pk)

        if product.favourites.filter(id=request.user.id).exists():
            product.favourites.remove(request.user)
            message =  'The product successfully deleted from your favourite list 😉'
            added = False

        else:
            product.favourites.add(request.user)
            message =  'The product successfully added to your favourite list 😉'
            added = True
        favourite_count = request.user.favourite.count()
        return JsonResponse({'message':message, 'added':added,'favourite_count':favourite_count})
    return JsonResponse({'error':'Invalid Request method '}, status=405)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    logo = NavbarIcons.objects.all()
    favourite_count = request.user.favourite.count()
    phone_numbers = ProductUserPhoneNumber.objects.filter(product=product)
    profile  = Profile.objects.get(user=request.user)
    comments = product.comments.all()
    comment_form = CommentForm()
    related_product = Product.objects.filter(option=product.option).exclude(pk=product_id)
    

    
    return render(request, 'core/product_detail.html',{'product':product,'logo':logo,'favourite_count':favourite_count,'profile':profile, 'phone_numbers':phone_numbers, 'comments':comments,'comment_form':comment_form, 'related_product':related_product})


@csrf_exempt
def product_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            
            return JsonResponse({'success':True, 'comment':comment.content, 'user':comment.user.username})
    
    return JsonResponse({'success':False})


def delete_product(request, product_id):
    logo = NavbarIcons.objects.all()
    product = get_object_or_404(Product, id=product_id)
    favourite_count = request.user.favourite.count()
    profile  = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        product.delete()
        
        return redirect('/user/'+str(request.user.username))
    
    return render(request, 'core/confirm_delete.html',{'logo':logo,'favourite_count':favourite_count,'profile':profile,'product':product})


def update_profile(request, product_id):
    product = Product.objects.get(id=product_id)
    favourite_count = request.user.favourite.count()
    profile  = Profile.objects.get(user=request.user)
    logo = NavbarIcons.objects.all()
    phone_number_instance = ProductUserPhoneNumber.objects.get(product=product)
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        
        product_form = ProductForm(request.POST, instance=product)
        phone_number_form = ProductUserPhoneNumberForm(request.POST, instance=phone_number_instance)
        
        if product_form.is_valid() and phone_number_form.is_valid():
            product_form.save()
            phone_number_form.save()
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            
            return redirect('/user/'+str(request.user))
    else:
        product_form = ProductForm(instance=product)
        phone_number_form = ProductUserPhoneNumberForm(instance=phone_number_instance)

    return render(request, 'core/product_update.html',{'product':product, 'phone_number_form':phone_number_form, 'product_form':product_form, 'favourite_count':favourite_count,'profile':profile,'logo':logo})