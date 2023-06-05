from django.shortcuts import render, redirect, get_object_or_404
from .models import Welfare
from django.utils import timezone


def mainpage(request):
    welfares = Welfare.objects.all()
    num_length = welfares.count()
    middle = num_length // 2

    first = welfares[:middle]
    second = welfares[middle:]
    return render(request, 'welfare/mainpage.html', {
        'welfares':welfares,
        'first':first,
        'second':second,
        })


def create(request):
    new_welfare = Welfare()
    new_welfare.title = request.POST['title']
    new_welfare.writer = request.user
    new_welfare.pub_date = timezone.now()
    new_welfare.image = request.FILES.get('image')
    new_welfare.body = request.POST['body']

    new_welfare.save()
    
    return redirect('welfare:detail', new_welfare.id)

def new(request):
    return render(request, 'welfare/new.html')


def detail(request, id):
    welfare = get_object_or_404(Welfare, pk = id)
    return render(request, 'welfares/detail.html',{
        'welfare':welfare
        })


def delete(request, id):
    delete_welfare = Welfare.objects.get(id = id)
    delete_welfare.delete()
    return redirect('welfare:mainpage')

def mainpage_likes(request, welfare_id):
    if request.user.is_authenticated:
        welfare = get_object_or_404(Welfare, id=welfare_id)
        if request.user in welfare.welfare_like.all():
            welfare.welfare_like.remove(request.user)
            welfare.welfare_like_count -=1
            welfare.save()
        else:
            welfare.welfare_like.add(request.user)
            welfare.welfare_like_count +=1
            welfare.save()
        return redirect('welfare:mainpage')
    else:
        return render(request, 'accounts/no_auth.html')


def detail_likes(request, welfare_id):
    if request.user.is_authenticated:
        welfare = get_object_or_404(Welfare, id=welfare_id)
        if request.user in welfare.welfare_like.all():
            welfare.welfare_like.remove(request.user)
            welfare.welfare_like_count -=1
            welfare.save()
        else:
            welfare.welfare_like.add(request.user)
            welfare.welfare_like_count +=1
            welfare.save()
        return redirect('welfare:detail', welfare.id)
    else:
        return render(request, 'accounts/no_auth.html')

