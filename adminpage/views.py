from django.shortcuts import render
from accounts.models import CustomUser

# Create your views here.
def user_admin(request):
    waiting_users = CustomUser.objects.filter(is_approved=False)
    approved_users = CustomUser.objects.filter(is_approved=True)
    staff_users = CustomUser.objects.filter(is_staff = True)
    context = {'waiting_users': waiting_users, 'approved_users':approved_users, 'staff_users':staff_users}
    return render(request, 'adminpage/user_admin.html', context)