from django.shortcuts import render, redirect, get_object_or_404
from .models import Benefit
from django.utils import timezone


def mainpage(request):
    benefits = Benefit.objects.all()
    num_length = benefits.count()
    middle = num_length // 2

    first = benefits[:middle]
    second = benefits[middle:]
    return render(request, 'benefits/mainpage.html', {
        'benefits':benefits,
        'first':first,
        'second':second,
        })


def create(request):
    new_benefit = Benefit()
    new_benefit.title = request.POST['title']
    new_benefit.writer = request.user
    new_benefit.pub_date = timezone.now()
    new_benefit.image = request.FILES.get('image')
    new_benefit.body = request.POST['body']

    new_benefit.save()
    
    return redirect('benefits:detail', new_benefit.id)

def new(request):
    return render(request, 'benefits/new.html')

def detail(request, id):
    benefit = get_object_or_404(Benefit, pk = id)
    return render(request, 'benefits/detail.html',{
        'benefit':benefit,
        })


def delete(request, id):
    delete_benefits = Benefit.objects.get(id = id)
    delete_benefits.delete()
    return redirect('benefits:mainpage')

def mainpage_likes(request, benefit_id):
    if request.user.is_authenticated:
        benefit = get_object_or_404(Benefit, id=benefit_id)
        if request.user in benefit.benefit_like.all():
            benefit.benefit_like.remove(request.user)
            benefit.benefit_like_count -=1
            benefit.save()
        else:
            benefit.benefit_like.add(request.user)
            benefit.benefit_like_count +=1
            benefit.save()
        return redirect('benefits:mainpage')
    else:
        return render(request, 'accounts/no_auth.html')


def detail_likes(request, benefit_id):
    if request.user.is_authenticated:
        benefit = get_object_or_404(Benefit, id=benefit_id)
        if request.user in benefit.benefit_like.all():
            benefit.benefit_like.remove(request.user)
            benefit.benefit_like_count -=1
            benefit.save()
        else:
            benefit.benefit_like.add(request.user)
            benefit.benefit_like_count +=1
            benefit.save()
        return redirect('benefits:detail', benefit.id)
    else:
        return render(request, 'accounts/no_auth.html')

