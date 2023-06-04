from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    writer = models.ForeignKey(CustomUser, on_delete = models.CASCADE )
    pub_date = models.DateTimeField()
    body = models.TextField()
    like = models.ManyToManyField(CustomUser, related_name='likes', blank = True)
    like_count = models.PositiveIntegerField(default = 0)
    
    def __str__(self):
        return self.title
    
    def summary(self):
        return self.body[:20]
    
    