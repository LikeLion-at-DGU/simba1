from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Benefit(models.Model):
    title = models.CharField(max_length=200)
    writer = models.ForeignKey(CustomUser, on_delete = models.CASCADE )
    start_date = models.DateTimeField(null = True, blank = True)
    due_date = models.DateTimeField(null = True, blank = True)
    body = models.TextField()
    image = models.ImageField(upload_to='benefits/', null = True, blank = True)
    benefit_like = models.ManyToManyField(CustomUser, related_name = 'benefit_likes', blank = True)
    benefit_like_count = models.PositiveIntegerField(default = 0)
    
    def __str__(self):
        return self.title
    
    def summary(self):
        return self.body[:20]
    

