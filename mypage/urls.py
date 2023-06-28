from django.urls import path
from .views import *

app_name = "mypage"
urlpatterns = [
    path('information/', information, name="information"),
    path('scrap/', scrap, name="scrap"),
    path('my_comment/', my_comment, name="my_comment"),
    path('postmanagement/', postmanagement, name="postmanagement"),
    path('staff_postmanagement/', staff_postmanagement, name="staff_postmanagement"),
    path('super_benefit_detail/<int:benefit_id>', super_benefit_detail, name="super_benefit_detail"),
    path('super_welfare_detail/<int:welfare_id>', super_welfare_detail, name="super_welfare_detail"),
    path('super_main_detail/<int:mainpost_id>', super_main_detail, name="super_main_detail"),
    path('staff_benefit_detail/<int:benefit_id>', staff_benefit_detail, name="staff_benefit_detail"),
    path('staff_welfare_detail/<int:welfare_id>', staff_welfare_detail, name="staff_welfare_detail"),
    path('staff_main_detail/<int:mainpost_id>', staff_main_detail, name="staff_main_detail"),
    path('benefit_delete_comment/<int:comment_id>', benefit_delete_comment, name="benefit_delete_comment"),
    path('welfare_delete_comment/<int:comment_id>', welfare_delete_comment, name="welfare_delete_comment"),
    path('mainpost_delete_comment/<int:comment_id>', mainpost_delete_comment, name="mainpost_delete_comment"),
    path('change_nickname/', change_nickname, name="change_nickname"),
    path('user_delete/', user_delete, name="user_delete"),
]