from django.db import models
from accounts.models import CustomUser

# Create your models here.
class MainPost(models.Model):
    title = models.CharField(max_length=20, blank = False, null = False) #제휴 상점 이름
    writer = models.ForeignKey(CustomUser, on_delete = models.CASCADE) #게시물 작성자
    pub_date = models.DateTimeField()
    start_time = models.TimeField(null = True, blank = True, default = None) #제휴 상점 운영 시작 시간
    end_time = models.TimeField(null = True, blank = True, default = None) #제휴 상점 운영 종료 시간
    address = models.CharField(max_length = 30, blank = False, null = False) #제휴 상점 주소
    category_type = models.CharField(max_length = 50, null = False, blank = False) #식당, 주점, 의료 ...카테고리
    body = models.TextField(blank = False, null = False) #게시물 내용
    image = models.ImageField(upload_to='mainposts/', null = True, blank = True) #게시물에 들어가는 사진
    mainpost_like = models.ManyToManyField(CustomUser, related_name = 'mainpost_likes', blank = True) #게시물 좋아요 기능
    mainpost_like_count = models.PositiveIntegerField(default = 0) #게시물 좋아요 개수
    mainpost_rate_average = models.DecimalField(default = 0, max_digits = 2, decimal_places = 1) #게시물 평점 평균

    
    def __str__(self):
        return self.title
    
    def summary(self):
        return self.body[:20]
    
    
class MainComment(models.Model):
    mainpost = models.ForeignKey(MainPost, on_delete = models.CASCADE, blank = False, null = False)
    mainpost_rate = models.IntegerField(default = 0) #댓글 평점
    content = models.TextField(blank = False, null = False) #댓글 내용
    pub_date = models.DateTimeField() #댓글 작성날짜
    writer = models.ForeignKey(CustomUser, on_delete = models.CASCADE, blank = False, null = False)
    comment_like = models.ManyToManyField(CustomUser, related_name = 'mainpost_comment_likes', blank = True) #댓글 좋아요 기능
    comment_like_count = models.IntegerField(default = 0) #댓글 좋아요 개수

    def save(self, *args, **kwargs): #댓글을 추가하는 동시에 게시물 평균 평점 변하도록
        super().save(*args, **kwargs) #코멘트 세이브 하면
        mainpost = self.mainpost #이 댓글이 있는 게시물 가져와서
        comments = MainComment.objects.filter(mainpost = mainpost) #게시물에 있는 댓글들 모두 불러옴
        rate_sum = 0 #평점 평균을 내기 위해 평점 합을 우선 0으로 맞춤

        for comment in comments:
            rate_sum = rate_sum + comment.mainpost_rate #0부터 시작해서 댓글들에 있는 평점을 모두 더함
        rate_total = len(comments) #댓글들 개수
        mainpost_rate_average = rate_sum / rate_total #평균 구함

        mainpost.mainpost_rate_average = mainpost_rate_average #평균값 게시물 필드값에 담음
        mainpost.save() #이상태로 게시물 저장
    
    def delete(self, *args, **kwargs): #이거는 댓글 삭제했을 때
        mainpost = self.mainpost
        super().delete(*args, **kwargs)
        comments = MainComment.objects.filter(mainpost = mainpost)
        rate_sum = 0

        for comment in comments:
            rate_sum = rate_sum + comment.mainpost_rate
        rate_total = len(comments)
        mainpost_rate_average = rate_sum / rate_total 

        mainpost.mainpost_rate_average = mainpost_rate_average
        mainpost.save()
        
    def __str__(self):
        return self.mainpost.title + ':' + self.content[:10] + '평점' + self.mainpost_rate