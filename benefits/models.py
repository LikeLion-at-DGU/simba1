from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Benefit(models.Model):
    title = models.CharField(max_length=20) #제휴 상점 이름
    writer = models.ForeignKey(CustomUser, on_delete = models.CASCADE) #게시물 작성자
    start_time = models.TimeField() #제휴 상점 운영 시작 시간
    end_time = models.TimeField() #제휴 상점 운영 종료 시간
    address = models.CharField(max_length = 30) #제휴 상점 주소
    start_date = models.DateField(null = True, blank = True) #제휴혜택 시작 날짜
    end_date = models.DateField(null = True, blank = True) #제휴혜택 종료 날짜
    category_univ = models.CharField(max_length = 50, null = False, blank = False) #단과대학 카테고리
    category_type = models.CharField(max_length = 50, null = False, blank = False) #식당, 주점, 의료 ...카테고리
    body = models.TextField() #게시물 내용
    image = models.ImageField(upload_to='benefits/', null = True, blank = True) #게시물에 들어가는 사진
    benefit_like = models.ManyToManyField(CustomUser, related_name = 'benefit_likes', blank = True) #게시물 좋아요 기능
    benefit_like_count = models.PositiveIntegerField(default = 0) #게시물 좋아요 개수
    benefit_rate_average = models.DecimalField(default = 0, max_digits = 2, decimal_places = 1) #게시물 평점 평균

    
    def __str__(self):
        return self.title
    
    def summary(self):
        return self.body[:20]
    
class BComment(models.Model):
    benefit = models.ForeignKey(Benefit, on_delete = models.CASCADE, blank = False, null = False)
    benefit_rate = models.IntegerField(default = 0) #댓글 평점
    content = models.TextField() #댓글 내용
    pub_date = models.DateTimeField() #댓글 작성날짜
    writer = models.ForeignKey(CustomUser, on_delete = models.CASCADE, blank = False, null = False)
    comment_like = models.ManyToManyField(CustomUser, related_name = 'comment_likes', blank = True) #댓글 좋아요 기능
    comment_like_count = models.IntegerField(default = 0) #댓글 좋아요 개수

    def save(self, *args, **kwargs): #댓글을 추가하는 동시에 게시물 평균 평점 변하도록
        super().save(*args, **kwargs) #코멘트 세이브 하면
        benefit = self.benefit #이 댓글이 있는 게시물 가져와서
        comments = BComment.objects.filter(benefit = benefit) #게시물에 있는 댓글들 모두 불러옴
        rate_sum = 0 #평점 평균을 내기 위해 평점 합을 우선 0으로 맞춤

        for comment in comments:
            rate_sum = rate_sum + comment.benefit_rate #0부터 시작해서 댓글들에 있는 평점을 모두 더함
        rate_total = len(comments) #댓글들 개수
        benefit_rate_average = rate_sum / rate_total #평균 구함

        benefit.benefit_rate_average = benefit_rate_average #평균값 게시물 필드값에 담음
        benefit.save() #이상태로 게시물 저장
    
    def delete(self, *args, **kwargs): #이거는 댓글 삭제했을 때
        benefit = self.benefit
        super().delete(*args, **kwargs)
        comments = BComment.objects.filter(benefit = benefit)
        rate_sum = 0

        for comment in comments:
            rate_sum = rate_sum + comment.benefit_rate
        rate_total = len(comments)
        benefit_rate_average = rate_sum / rate_total 

        benefit.benefit_rate_average = benefit_rate_average
        benefit.save()
        
    def __str__(self):
        return self.benefit.title + ':' + self.content[:10] + '평점' + self.benefit_rate
    

