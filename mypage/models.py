from django.db import models
from django.conf import settings
from main.models import Blog
from accounts.models import CustomUser

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    nickname = models.CharField(max_length = 200)
    department = models.CharField(max_length = 100)

    def __str__(self):
        return self.nickname