from django.shortcuts import render
from accounts.models import CustomUser

# Create your views here.
# 커스텀 어드민 페이지 유저 목록
def user_admin(request):
    if request.user.is_superuser:
        waiting_users = CustomUser.objects.filter(is_approved=False) #승인 안된 유저 담아담아
        return render(request, 'adminpage/user_approval.html', {
            'waiting_users' : waiting_users,
            })
    else:
        return render(request, 'accounts/no_auth.html')

def staff_admin(request):
    if request.user.is_superuser:
        approved_users = CustomUser.objects.filter(is_approved = True)
        staff_users = CustomUser.objects.filter(is_staff = True)
        return render(request, 'adminpage/staff_admin.html',{
            'approved_users' : approved_users,
            'staff_users' : staff_users,
        })
    else:
        return render(request, 'accounts/no_auth.html')

def user_image(request, user_id):
    if request.user.is_superuser:
        user = CustomUser.objects.get(id = user_id)
        return render(request, 'adminpage/user_image.html', {
            'user' : user,
        })
    else:
        return render(request, 'accounts/no_auth.html')
