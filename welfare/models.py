from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Welfare(models.Model):
    title = models.CharField(max_length=200)
    writer = models.ForeignKey(CustomUser, on_delete = models.CASCADE )
    start_time = models.TimeField(null = True) # 영업시간_시작
    end_time = models.TimeField(null = True) # 영업시간_끝
    address = models.CharField(max_length = 30) # 주소
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    category_univ = models.CharField(max_length=50, null = False, blank = True) # 게시판 선택
    category_type = models.CharField(max_length=50, null = False, blank = True) # 카테고리
    body = models.TextField()
    image = models.ImageField(upload_to='welfare/')
    welfare_like = models.ManyToManyField(CustomUser, related_name='welfare_likes', blank = True)
    welfare_like_count = models.PositiveIntegerField(default = 0)
    


    def __str__(self):
        return self.title
    
    def summary(self):
        return self.body[:20]