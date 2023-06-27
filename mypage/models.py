from django.db import models
from django.conf import settings
from accounts.models import CustomUser

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    nickname = models.CharField(max_length = 200)
    univ = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'user_image/', null = True, blank = True) #유저 인증 이미지

    def __str__(self):
        return self.nickname