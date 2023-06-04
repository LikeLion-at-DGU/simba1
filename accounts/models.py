from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.S
class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to = 'user_image/')


