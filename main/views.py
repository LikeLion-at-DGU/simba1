from django.shortcuts import render, redirect, get_object_or_404
from benefits.models import Benefit
from welfare.models import Welfare
from django.utils import timezone


def intro(request):
    return render(request, 'main/intro.html')

def mainpage(request):
    return render(request, 'main/mainpage.html')


def benefits_likes(request, benefit_id):
    if request.user.is_authenticated:
        benefit = get_object_or_404(Benefit, id=benefit_id)
        if request.user in benefit.like.all():
            benefit.like.remove(request.user)
            benefit.like_count -=1
            benefit.save()
        else:
            benefit.like.add(request.user)
            benefit.like_count +=1
            benefit.save()
        return redirect('main:mainpage', benefit.id)
    else:
        return render(request, 'accounts/no_auth.html')

