

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from .models import CustomUser
from mypage.models import Profile
from benefits.models import Benefit
from welfare.models import Welfare

# Create your views here.
# 유저 로그인
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
    
# 유저 로그아웃
def logout(request):
    auth.logout(request)
    return redirect('main:mainpage')
    
# 유저 회원가입
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

# 유저 회원가입 완료
def signup_completed(request):
    return render(request, 'accounts/sign-up-completed.html')

# 유저 회원가입 시 이미지 인증
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

# 어드민 페이지
# 유저 승인
def approve_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_approved = True
    user.save()
    return redirect('adminpage:user_admin')

# 유저 삭제
def delete_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    blogs = Benefit.objects.filter(like=user)
    for blog in blogs:
        blog.like.remove(user)
        blog.like_count -=1
    user.image.delete()
    user.delete()
    return redirect('adminpage:user_admin')

# 유저 승인 취소
def cancel_approval(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_approved = False
    user.is_staff = False
    user.save()
    return redirect('adminpage:user_admin')

# 유저 스태프 권한 승인
def approve_staff(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_staff = True
    user.save()
    return redirect('adminpage:user_admin')

# 유저 스태프 권한 취소
def cancel_staff(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_staff = False
    user.save()
    return redirect('adminpage:user_admin')

