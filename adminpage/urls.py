from django.urls import path
from .views import *

app_name = "adminpage"

urlpatterns = [
    path('user_admin/', user_admin, name='user_admin'),
    path('user_image/<int:user_id>', user_image, name="user_image"),
    path('staff_admin/', staff_admin, name="staff_admin"),
]