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
        username = request.POST['username'] #로그인 창에서 쓴 id값 담아담아
        password = request.POST['password'] #로그인 창에서 쓴 pw값 담아담아
        user = auth.authenticate(request, username=username, password=password) #User 모델 안에 있는 username 하고 password 값하고 비교해서 같지 않으면 None 값 반환

        if user is not None: # None 값이 반환이 안된다면
            if user.is_approved == True: #승인된 유저라면
                if user.is_approved is not None: # 이건 내가 왜 써놓은거지... 나중에 한 번 봐야할듯
                    auth.login(request, user)
                    return redirect('main:mainpage')
            else:
                return render(request, 'accounts/no_approval.html') #승인 안되있으면 오류 메세지 띄움
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

            user = CustomUser.objects.create_user(username=request.POST['username'], password=request.POST['password'],) #CustomUser 모델에 user 생성
            user.save() #저장
            nickname = request.POST['nickname']
            department = request.POST['department']
            
            profile = Profile(user = user, nickname = nickname, department = department)
            profile.save()


            return redirect('accounts:image_verification', user.id) #유저 이미지 인증 페이지로 넘어감.
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
            return redirect('accounts:image_verification', user.id) #이미지 없으면 다시 이미지 인증 페이지로 넘어감.
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
    blogs = Benefit.objects.filter(benefit_like=user)
    for blog in blogs: #이게 유저 삭제 시 좋아요 개수도 줄어들게 하는 건데 왜 안되는 지 모르겠뜸.
        blog.benefit_like.remove(user)
        blog.benefit_like_count -=1
    user.image.delete() #유저 삭제시 인증할 때 받은 사진도 같이 삭제
    user.delete() #유저 삭제
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

