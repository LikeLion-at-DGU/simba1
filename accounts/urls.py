from django.urls import path
from .views import *

app_name = "accounts"
urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('signup/', signup, name="signup"),
    path('approve/<int:user_id>/', approve_user, name='approve_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('cancel_approval/<int:user_id>/', cancel_approval, name='cancel_approval'),
    path('approve_staff/<int:user_id>/', approve_staff, name='approve_staff'),
    path('cancel_staff/<int:user_id>/', cancel_staff, name='cancel_staff'),
    path('image_verification/<int:user_id>', image_verification, name="image_verification"),
    path('signup_completed/', signup_completed, name="signup_completed"),
]