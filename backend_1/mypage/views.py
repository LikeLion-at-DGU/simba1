# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from benefits.models import Benefit, BComment
from welfare.models import Welfare

# Create your views here.
def information(request):
    user = request.user
    benefits = Benefit.objects.filter(writer = user) #게시물 작성자가 현재 로그인한 유저와 같은 것들만 가져옴
    post_first_line = []
    post_second_line = []

    for i, benefit in enumerate(benefits): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(benefit) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(benefit) #담아담아

    return render(request, 'mypage/information.html', {
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
    })

def scrap(request): #스크랩 기능
    user = request.user
    benefits = Benefit.objects.filter(benefit_like = user) #좋아요한 게시물 중에 유저가 있는 게시물들
    welfares = Welfare.objects.filter(welfare_like = user)

    return render(request, 'mypage/scrap.html', {
        'benefits':benefits,
        'welfares':welfares,
        })

def my_comment(request):
    user = request.user
    comments = BComment.objects.filter(writer = user)
    return render(request, 'mypage/my_comment.html',{
        'comments':comments,
    })

def scrap_benefits_likes(request, benefit_id): #스크랩 안에서 좋아요 누를 때
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
    
def mypage_benefits_likes(request, benefit_id): #마이페이지 안에서 좋아요 누를 때
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
        return redirect('mypage:information')
    else:
        return render(request, 'accounts/no_auth.html')