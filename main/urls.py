from django.urls import path
from .views import *

app_name = "main"
urlpatterns = [
    path('', intro, name="intro"),
    path('mainpage/', mainpage, name="mainpage"),
]