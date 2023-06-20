from django.urls import path
from .views import *

app_name = "adminpage"

urlpatterns = [
    path('user_admin/', user_admin, name='user_admin'),
    path('user_image/<int:id>', user_image, name="user_image"),
]