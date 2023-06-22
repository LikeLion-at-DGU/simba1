from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# 찐 관리자 페이지에서 유저 승인
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'is_active', 'is_approved']
    list_filter = ['is_active', 'is_approved']
    actions = ['approve_users'] #approve_users 라는 명령을 내림

    def approve_users(self, request, queryset): #approve_users라는 명령어 실행시
        queryset.update(is_approved=True) #유저 승인 시 is_approved 필드값 True로 변경

    approve_users.short_description = "유저 승인" 

admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
