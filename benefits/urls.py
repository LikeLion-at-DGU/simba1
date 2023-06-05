from django.urls import path
from .views import *

app_name = "benefits"
urlpatterns = [
    path('mainpage/', mainpage, name="mainpage"),
    path('new/', new, name="new"),
    path('create/', create, name="create"),
    path('delete/<int:id>', delete, name="delete"),
    path('<int:id>', detail, name="detail"),
    path('benefits_likes/<int:benefit_id>', mainpage_likes, name="mainpage_likes"),
    path('likes/<int:benefit_id>', detail_likes, name="detail_likes"),
]