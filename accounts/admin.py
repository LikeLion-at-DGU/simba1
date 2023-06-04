from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'is_active', 'is_approved']
    list_filter = ['is_active', 'is_approved']
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)

    approve_users.short_description = "Approve selected users"

admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
