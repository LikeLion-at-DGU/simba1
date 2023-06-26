# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from benefits.models import Benefit, BComment
from welfare.models import Welfare

# Create your views here.
def information(request):
    if request.user.is_authenticated:
        return render(request, 'mypage/information.html')
    else:
        return render(request, 'accounts/no_auth.html')
    
def postmanagement(request):
    if request.user.is_staff:
        user = request.user
        benefits = Benefit.objects.filter(writer = user) #게시물 작성자가 현재 로그인한 유저와 같은 것들만 가져옴

        return render(request, 'mypage/postmanagement.html', {
            'benefits' : benefits,
        })
    else:
        return render(request, 'accounts/no_auth.html')
    
def staff_postmanagement(request):
    if request.user.is_superuser:
        staff_posts = Benefit.objects.filter(writer__is_staff = True)

        return render(request, 'mypage/postmanagement.html', {
            'staff_posts' : staff_posts,
        })

def scrap(request): #스크랩 기능
    if request.user.is_authenticated:
        user = request.user
        benefits = Benefit.objects.filter(benefit_like = user) #좋아요한 게시물 중에 유저가 있는 게시물들
        welfares = Welfare.objects.filter(welfare_like = user)

        benefit_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
        benefit_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
        welfare_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
        welfare_second_line = []

        for i, benefit in enumerate(benefits): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                benefit_first_line.append(benefit) #담아담아
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                benefit_second_line.append(benefit) #담아담아

        if len(benefit_second_line) < len(benefit_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
            for i, welfare in enumerate(welfares):
                if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                    welfare_second_line.append(welfare)
                elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                    welfare_first_line.append(welfare) #담아담아
        else:
            for i, welfare in enumerate(welfares):
                if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                    welfare_first_line.append(welfare)
                elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                    welfare_second_line.append(welfare) #담아담아

        return render(request, 'mypage/scrap.html', {
            'benefit_first_line' : benefit_first_line,
            'benefit_second_line' : benefit_second_line,
            'welfare_first_line' : welfare_first_line,
            'welfare_second_line' : welfare_second_line,
            })
    else:
        return render(request, 'accounts/no_auth.html')

def my_comment(request):
    if request.user.is_authenticated:
        user = request.user
        comments = BComment.objects.filter(writer = user)
        return render(request, 'mypage/my_comment.html',{
            'comments' : comments,
        })
    else:
        return redirect('accounts:login')

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