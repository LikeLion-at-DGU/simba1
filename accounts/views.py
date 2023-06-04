

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from .models import CustomUser
from mypage.models import Profile
from main.models import Blog

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_approved == True:
                if user.is_approved is not None:
                    auth.login(request, user)
                    return redirect('main:mainpage')
            else:
                return render(request, 'accounts/no_approval.html')
        else:
            return render(request, 'accounts/login.html')
    
    elif request.method == 'GET':
        return render(request, 'accounts/login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('main:mainpage')
    
def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm']:

            user = CustomUser.objects.create_user(username=request.POST['username'], password=request.POST['password'],)
            user.save()
            nickname = request.POST['nickname']
            department = request.POST['department']
            
            profile = Profile(user = user, nickname = nickname, department = department)
            profile.save()


            return redirect('accounts:image_verification', user.id)
    return render(request, 'accounts/signup.html')

def signup_completed(request):
    return render(request, 'accounts/sign-up-completed.html')

def image_verification(request, id):
    user = get_object_or_404(CustomUser, pk = id)
    if request.method == 'POST':
        user.image = request.FILES.get('image_verification')
        if user.image:
            user.save()
            return redirect('accounts:signup_completed')
        else:
            return redirect('accounts:image_verification', user.id)
    return render(request, 'accounts/verification.html', {'user':user})


def approve_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_approved = True
    user.save()
    return redirect('adminpage:user_admin')

def delete_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    blogs = Blog.objects.filter(like=user)
    for blog in blogs:
        blog.like.remove(user)
        blog.like_count -=1
    user.image.delete()
    user.delete()
    return redirect('adminpage:user_admin')

def cancel_approval(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_approved = False
    user.is_staff = False
    user.save()
    return redirect('adminpage:user_admin')

def approve_staff(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_staff = True
    user.save()
    return redirect('adminpage:user_admin')

def cancel_staff(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_staff = False
    user.save()
    return redirect('adminpage:user_admin')

