# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from benefits.models import Benefit
from welfare.models import Welfare

# Create your views here.
def information(request):
    return render(request, 'mypage/information.html')

def scrap(request):
    user = request.user
    benefits = Benefit.objects.filter(benefit_like = user)
    welfares = Welfare.objects.filter(welfare_like = user)

    return render(request, 'mypage/scrap.html', {
        'benefits':benefits,
        'welfares':welfares,
        })

def mypage_benefits_likes(request, benefit_id):
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
        return redirect('mypage:scrap')
    else:
        return render(request, 'accounts/no_auth.html')