from django.urls import path
from .views import *

app_name = "welfare"
urlpatterns = [
    path('mainpage/', mainpage, name="mainpage"),
    path('new/', new, name="new"),
    path('create/', create, name="create"),
    path('delete/<int:id>', delete, name="delete"),
    path('<int:id>', detail, name="detail"),
    path('welfare_likes/<int:welfare_id>', mainpage_likes, name="mainpage_likes"),
    path('likes/<int:welfare_id>', detail_likes, name="detail_likes"),
]