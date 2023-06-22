from django.urls import path
from .views import *

app_name = "mypage"
urlpatterns = [
    path('information/', information, name="information"),
    path('scrap/', scrap, name="scrap"),
    path('my_comment/', my_comment, name="my_comment"),
    path('mypage_benefits_likes/<int:benefit_id>', mypage_benefits_likes, name="mypage_benefits_likes"),
    path('scrap_benefits_likes/<int:benefit_id>', scrap_benefits_likes, name="scrap_benefits_likes"),
]