from django.urls import path
from .views import *

app_name = "main"
urlpatterns = [
    path('', intro, name="intro"),
    path('mainpage/', mainpage, name="mainpage"),
    path('benefits/', benefits, name="benefits"),
    path('welfare/', welfare, name="welfare"),
    path('new/', new, name="new"),
    path('create/', create, name="create"),
    path('<int:id>', detail, name="detail"),
    path('likes/<int:blog_id>', likes, name="likes"),
]