from django.urls import path
from .views import *

app_name = "main"
urlpatterns = [
    path('', intro, name="intro"),
    path('mainpage/', mainpage, name="mainpage"),
    path('benefits_likes/<int:blog_id>', benefits_likes, name="benefits_likes"),
]