# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from benefits.models import Benefit, BComment
from welfare.models import Welfare, WComment
from main.models import MainPost, MainComment
from .models import Profile
from django.http import HttpResponse
import json

# Create your views here.
def information(request):
    if request.user.is_authenticated:
        return render(request, 'mypage/information.html')
    else:
        return render(request, 'accounts/no_auth.html')
    
def change_nickname(request):
    if request.method == 'GET':
        edit_user = request.user
        return render(request, 'mypage/change_nickname.html', {
            'edit_user' : edit_user,
        })
    elif request.method == 'POST':
        edit_user = request.user
        for user_profile in Profile.objects.all():
            if request.POST['nickname'] == user_profile.nickname:
                return render(request, 'mypage/change_nickname.html',{
                    'edit_user' : edit_user,
                })
        edit_user.profile.nickname = request.POST['nickname']
        edit_user.profile.save()
        return redirect('mypage:information')
    
def user_delete(request):
    if request.method == 'POST':
        password = request.POST['confirm_password']
        if request.user.check_password(password):
            request.user.delete()
            return redirect('main:mainpage')
        else:
            return render(request, 'mypage/user_delete.html')
    return render(request, 'mypage/user_delete.html')
    
def postmanagement(request):
    if request.user.is_staff:
        user = request.user
        benefits = Benefit.objects.filter(writer = user) #게시물 작성자가 현재 로그인한 유저와 같은 것들만 가져옴
        welfares = Welfare.objects.filter(writer = user)
        mainposts = MainPost.objects.filter(writer = user)

        return render(request, 'mypage/postmanagement.html', {
            'benefits' : benefits,
            'welfares' : welfares,
            'mainposts' : mainposts,
        })
    else:
        return render(request, 'accounts/no_auth.html')
    
def staff_postmanagement(request):
    if request.user.is_superuser:
        benefits = Benefit.objects.filter(writer__is_staff = True, writer__is_superuser = False)
        welfares = Welfare.objects.filter(writer__is_staff = True, writer__is_superuser = False)
        mainposts = MainPost.objects.filter(writer__is_staff = True, writer__is_superuser = False)
        
        return render(request, 'mypage/staffpostmanagement.html', {
            'benefits' : benefits,
            'welfares' : welfares,
            'mainposts' : mainposts,
        })

def scrap(request): #스크랩 기능
    if request.user.is_authenticated:
        user = request.user
        benefits = Benefit.objects.filter(benefit_like = user) #좋아요한 게시물 중에 유저가 있는 게시물들
        welfares = Welfare.objects.filter(welfare_like = user)
        mainposts = MainPost.objects.filter(mainpost_like = user)

        benefit_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
        benefit_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
        welfare_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
        welfare_second_line = []
        mainpost_first_line = []
        mainpost_second_line = []

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

            if (len(benefits) + len(welfares)) % 2 == 1:
                for i, mainpost in enumerate(mainposts):
                    if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                        mainpost_second_line.append(mainpost)
                    elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                        mainpost_first_line.append(mainpost) #담아담아
            elif (len(benefits) + len(welfares)) % 2 == 0:
                for i, mainpost in enumerate(mainposts):
                    if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                        mainpost_first_line.append(mainpost)
                    elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                        mainpost_second_line.append(mainpost) #담아담아
        else:
            for i, welfare in enumerate(welfares):
                if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                    welfare_first_line.append(welfare)
                elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                    welfare_second_line.append(welfare) #담아담아

            if (len(benefits) + len(welfares)) % 2 == 1:
                for i, mainpost in enumerate(mainposts):
                    if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                        mainpost_second_line.append(mainpost)
                    elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                        mainpost_first_line.append(mainpost) #담아담아
            elif (len(benefits) + len(welfares)) % 2 == 0:
                for i, mainpost in enumerate(mainposts):
                    if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                        mainpost_first_line.append(mainpost)
                    elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                        mainpost_second_line.append(mainpost) #담아담아

        return render(request, 'mypage/scrap.html', {
            'benefit_first_line' : benefit_first_line,
            'benefit_second_line' : benefit_second_line,
            'welfare_first_line' : welfare_first_line,
            'welfare_second_line' : welfare_second_line,
            'mainpost_first_line' : mainpost_first_line,
            'mainpost_second_line' : mainpost_second_line,
            })
    else:
        return render(request, 'accounts/no_auth.html')

def my_comment(request):
    if request.user.is_authenticated:
        user = request.user
        benefit_comments = BComment.objects.filter(writer = user)
        welfare_comments = WComment.objects.filter(writer = user)
        mainpost_comments = MainComment.objects.filter(writer = user)
        return render(request, 'mypage/my_comment.html',{
            'benefit_comments' : benefit_comments,
            'welfare_comments' : welfare_comments,
            'mainpost_comments' : mainpost_comments,
        })
    else:
        return redirect('accounts:login')
    
def benefit_delete_comment(request, comment_id):
    delete_comment = BComment.objects.get(id = comment_id)
    if request.user == delete_comment.writer:
        delete_comment.delete()
        return redirect('mypage:my_comment')
    elif request.user.is_superuser:
        delete_comment.delete()
        return redirect('mypage:my_comment')
    else:
        return render(request, 'accounts/no_auth.html')
    
def welfare_delete_comment(request, comment_id):
    delete_comment = WComment.objects.get(id = comment_id)
    if request.user == delete_comment.writer:
        delete_comment.delete()
        return redirect('mypage:my_comment')
    elif request.user.is_superuser:
        delete_comment.delete()
        return redirect('mypage:my_comment')
    else:
        return render(request, 'accounts/no_auth.html')
    
def mainpost_delete_comment(request, comment_id):
    delete_comment = MainComment.objects.get(id = comment_id)
    if request.user == delete_comment.writer:
        delete_comment.delete()
        return redirect('mypage:my_comment')
    elif request.user.is_superuser:
        delete_comment.delete()
        return redirect('mypage:my_comment')
    else:
        return render(request, 'accounts/no_auth.html')
    
def super_benefit_detail(request, benefit_id):
    benefit = get_object_or_404(Benefit, pk = benefit_id)
    comments = BComment.objects.filter(benefit = benefit)
    comments_count = len(comments)
    return render(request, 'mypage/super_benefit_detail.html',{
        'benefit' : benefit,
        'comments' : comments,
        'comments_count' : comments_count,
        })


def super_welfare_detail(request, welfare_id):
    welfare = get_object_or_404(Welfare, pk = welfare_id)
    comments = WComment.objects.filter(welfare = welfare)
    comments_count = len(comments)
    return render(request, 'mypage/super_welfare_detail.html',{
        'welfare' : welfare,
        'comments' : comments,
        'comments_count' : comments_count,
        })


def super_main_detail(request, mainpost_id):
    mainpost = get_object_or_404(MainPost, pk = mainpost_id)
    comments = MainComment.objects.filter(mainpost = mainpost)
    comments_count = len(comments)
    return render(request, 'mypage/super_main_detail.html',{
        'mainpost' : mainpost,
        'comments' : comments,
        'comments_count' : comments_count,
        })

def staff_benefit_detail(request, benefit_id):
    benefit = get_object_or_404(Benefit, pk = benefit_id)
    comments = BComment.objects.filter(benefit = benefit)
    comments_count = len(comments)
    return render(request, 'mypage/staff_benefit_detail.html',{
        'benefit' : benefit,
        'comments' : comments,
        'comments_count' : comments_count,
        })

def staff_welfare_detail(request, welfare_id):
    welfare = get_object_or_404(Welfare, pk = welfare_id)
    comments = WComment.objects.filter(welfare = welfare)
    comments_count = len(comments)
    return render(request, 'mypage/staff_welfare_detail.html',{
        'welfare' : welfare,
        'comments' : comments,
        'comments_count' : comments_count,
        })


def staff_main_detail(request, mainpost_id):
    mainpost = get_object_or_404(MainPost, pk = mainpost_id)
    comments = MainComment.objects.filter(mainpost = mainpost)
    comments_count = len(comments)
    return render(request, 'mypage/staff_main_detail.html',{
        'mainpost' : mainpost,
        'comments' : comments,
        'comments_count' : comments_count,
        })