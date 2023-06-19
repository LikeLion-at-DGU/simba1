from django.db import models
from django.contrib.auth.models import AbstractUser #이게 유저 승인을 할 때에는 일반 유저 모델을 쓰지 않고 AbstractUser을 쓴다고 함.



# Create your models here
# 유저 승인을 위한 모델
class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False) #유저 승인 필드(가입 시 디폴트 값 False)
    image = models.ImageField(upload_to = 'user_image/') #유저 인증 이미지


