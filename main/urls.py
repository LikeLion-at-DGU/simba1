from django.urls import path
from .views import *

app_name = "main"
urlpatterns = [
    path('', intro, name="intro"),
    path('mainpage/', mainpage, name="mainpage"),
    path('create/', create, name="create"),
    path('<int:mainpost_id>', detail, name="detail"),
    path('update/<int:mainpost_id>', update, name="update"),
    path('delete/<int:mainpost_id>', delete, name="delete"),
    path('review/<int:mainpost_id>', review, name="review"),
    path('comment_likes/<int:comment_id>', comment_likes, name="comment_likes"),
    path('delete_comment/<int:comment_id>', delete_comment, name="delete_comment"),
    path('edit_comment/<int:comment_id>', edit_comment, name="edit_comment"),
    path('detail_likes/<int:mainpost_id>', detail_likes, name="detail_likes"),
]