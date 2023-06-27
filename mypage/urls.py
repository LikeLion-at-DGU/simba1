from django.urls import path
from .views import *

app_name = "mypage"
urlpatterns = [
    path('information/', information, name="information"),
    path('scrap/', scrap, name="scrap"),
    path('my_comment/', my_comment, name="my_comment"),
    path('postmanagement/', postmanagement, name="postmanagement"),
    path('staff_postmanagement/', staff_postmanagement, name="staff_postmanagement"),
    path('benefit_delete_comment/<int:comment_id>', benefit_delete_comment, name="benefit_delete_comment"),
    path('welfare_delete_comment/<int:comment_id>', welfare_delete_comment, name="welfare_delete_comment"),
    path('mainpost_delete_comment/<int:comment_id>', mainpost_delete_comment, name="mainpost_delete_comment"),
    path('change_nickname/', change_nickname, name="change_nickname"),
    path('user_delete/', user_delete, name="user_delete"),
]