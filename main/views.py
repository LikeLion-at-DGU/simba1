from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from django.utils import timezone

def detail(request, id):
    blog = get_object_or_404(Blog, pk = id)
    return render(request, 'main/detail.html',{'blog':blog})

def intro(request):
    return render(request, 'main/intro.html')

def mainpage(request):
    return render(request, 'main/mainpage.html')

def welfare(request):
    blogs = Blog.objects.all()
    return render(request, 'main/welfare.html', {'blogs':blogs})

def benefits(request):
    return render(request, 'main/benefits.html')

def create(request):
    new_blog = Blog()
    new_blog.title = request.POST['title']
    new_blog.writer = request.user
    new_blog.pub_date = timezone.now()
    new_blog.body = request.POST['body']

    new_blog.save()
    
    return redirect('main:detail', new_blog.id)

def new(request):
    return render(request, 'main/new.html')

def likes(request, blog_id):
    if request.user.is_authenticated:
        blog = get_object_or_404(Blog, id=blog_id)
        if request.user in blog.like.all():
            blog.like.remove(request.user)
            blog.like_count -=1
            blog.save()
        else:
            blog.like.add(request.user)
            blog.like_count +=1
            blog.save()
        return redirect('main:detail', blog.id)
    else:
        return render(request, 'accounts/no_auth.html')

