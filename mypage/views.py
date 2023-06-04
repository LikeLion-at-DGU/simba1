from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from main.models import Blog

# Create your views here.
def information(request):
    user = request.user
    blogs = Blog.objects.filter(like = user)
    return render(request, 'mypage/information.html', {
        'blogs':blogs,
    })