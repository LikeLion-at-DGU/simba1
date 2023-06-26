from django.contrib import admin
from .models import MainPost, MainComment

# Register your models here.
admin.site.register(MainPost)
admin.site.register(MainComment)