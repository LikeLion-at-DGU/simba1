from django.urls import path
from .views import *

app_name = "mypage"
urlpatterns = [
    path('information/', information, name="information"),
    path('scrap/', scrap, name="scrap"),
    path('mypage_benefits_likes/<int:benefit_id>', mypage_benefits_likes, name="mypage_benefits_likes"),
]