from django.shortcuts import render
from accounts.models import CustomUser

# Create your views here.
# 커스텀 어드민 페이지 유저 목록
def user_admin(request):
    waiting_users = CustomUser.objects.filter(is_approved=False) #승인 안된 유저 담아담아
    approved_users = CustomUser.objects.filter(is_approved=True) #승인 된 유저 담아담아
    staff_users = CustomUser.objects.filter(is_staff = True) #스태프 유저 담아담아
    return render(request, 'adminpage/user_admin.html', {
        'waiting_users': waiting_users,
        'approved_users':approved_users,
        'staff_users':staff_users,
        })