from django.urls import path
from .views import *

app_name = "welfare"
urlpatterns = [
    path('choose/', choose, name="choose"),
    path('business/', business, name="business"),
    path('art/', art, name="art"),
    path('social/', social, name="social"),
    path('ai/', ai, name="ai"),
    path('engineering/', engineering, name="engineering"),
    path('buddhism/', buddhism, name="buddhism"),
    path('future/', future, name="future"),
    path('science/', science, name="science"),
    path('liberal/', liberal, name="liberal"),
    path('police/', police, name="police"),
    path('education/', education, name="education"),
    path('law/', law, name="law"),
    path('mainpage/', mainpage, name="mainpage"),
    path('new/', new, name="new"),
    path('create/', create, name="create"),
    path('delete/<int:id>', delete, name="delete"),
    path('<int:id>', detail, name="detail"),
    path('mainpage_likes/<int:welfare_id>', mainpage_likes, name="mainpage_likes"),
    path('likes/<int:welfare_id>', detail_likes, name="detail_likes"),
    path('<int:id>', detail, name="detail"),
    path('review/<int:welfare_id>', review, name="review"),
]