from django.shortcuts import render, redirect, get_object_or_404
from .models import Benefit, BComment
from accounts.models import CustomUser
from django.utils import timezone
from django.db.models import F
from django.http import HttpResponse
import json


def choose(request):
    return render(request, 'benefits/choose.html')

# 각 단과대학 게시물 뜨게 하는 함수
# 경영대학 전체 게시물
def business(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경영대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경영대학") | Benefit.objects.filter(end_date = None, category_univ = "경영대학") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "경영대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "경영대학") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#경영대학 식당 게시물
def business_restaurant(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경영대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경영대학", category_type = "식당") | Benefit.objects.filter(end_date = None, category_univ = "경영대학", category_type = "식당") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "경영대학", category_type = "식당").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "경영대학", category_type = "식당") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#경영대학 주점 게시물
def business_pub(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경영대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경영대학", category_type = "주점") | Benefit.objects.filter(end_date = None, category_univ = "경영대학", category_type = "주점") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "경영대학", category_type = "주점").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "경영대학", category_type = "주점") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#경영대학 카페 게시물
def business_cafe(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경영대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경영대학", category_type = "카페") | Benefit.objects.filter(end_date = None, category_univ = "경영대학", category_type = "카페") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "경영대학", category_type = "카페").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "경영대학", category_type = "카페") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#경영대학 교육 게시물
def business_education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경영대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경영대학", category_type = "교육") | Benefit.objects.filter(end_date = None, category_univ = "경영대학", category_type = "교육") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "경영대학", category_type = "교육").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "경영대학", category_type = "교육") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#경영대학 의료 게시물
def business_medical(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경영대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경영대학", category_type = "의료") | Benefit.objects.filter(end_date = None, category_univ = "경영대학", category_type = "의료") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "경영대학", category_type = "의료").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "경영대학", category_type = "의료") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#예술 대학
#예술 대학 전체 게시물
def art(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "예술대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "예술대학") | Benefit.objects.filter(end_date = None, category_univ = "예술대학") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "예술대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "예술대학") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#예술대학 식당 게시물
def art_restaurant(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "예술대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "예술대학", category_type = "식당") | Benefit.objects.filter(end_date = None, category_univ = "예술대학", category_type = "식당") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "예술대학", category_type = "식당").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "예술대학", category_type = "식당") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#예술대학 주점 게시물
def art_pub(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "예술대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "예술대학", category_type = "주점") | Benefit.objects.filter(end_date = None, category_univ = "예술대학", category_type = "주점") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "예술대학", category_type = "주점").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "예술대학", category_type = "주점") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#예술대학 카페 게시물
def art_cafe(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "예술대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "예술대학", category_type = "카페") | Benefit.objects.filter(end_date = None, category_univ = "예술대학", category_type = "카페") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "예술대학", category_type = "카페").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "예술대학", category_type = "카페") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#예술대학 교육 게시물
def art_education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "예술대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "예술대학", category_type = "교육") | Benefit.objects.filter(end_date = None, category_univ = "예술대학", category_type = "교육") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "예술대학", category_type = "교육").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "예술대학", category_type = "교육") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#예술대학 의료 게시물
def art_medical(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "예술대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "예술대학", category_type = "의료") | Benefit.objects.filter(end_date = None, category_univ = "예술대학", category_type = "의료") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "예술대학", category_type = "의료").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "예술대학", category_type = "의료") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#사회과학대학
#사회과학대학 전체 게시물
def social(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사회과학대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사회과학대학") | Benefit.objects.filter(end_date = None, category_univ = "사회과학대학") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "사회과학대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "사회과학대학") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#사회과학대학 식당 게시물
def social_restaurant(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사회과학대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사회과학대학", category_type = "식당") | Benefit.objects.filter(end_date = None, category_univ = "사회과학대학", category_type = "식당") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "사회과학대학", category_type = "식당").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "사회과학대학", category_type = "식당") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#사회과학대학 주점 게시물
def social_pub(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사회과학대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사회과학대학", category_type = "주점") | Benefit.objects.filter(end_date = None, category_univ = "사회과학대학", category_type = "주점") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "사회과학대학", category_type = "주점").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "사회과학대학", category_type = "주점") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#사회과학대학 카페 게시물
def social_cafe(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사회과학대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사회과학대학", category_type = "카페") | Benefit.objects.filter(end_date = None, category_univ = "사회과학대학", category_type = "카페") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "사회과학대학", category_type = "카페").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "사회과학대학", category_type = "카페") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#사회과학대학 교육 게시물
def social_education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사회과학대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사회과학대학", category_type = "교육") | Benefit.objects.filter(end_date = None, category_univ = "사회과학대학", category_type = "교육") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "사회과학대학", category_type = "교육").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "사회과학대학", category_type = "교육") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#사회과학대학 의료 게시물
def social_medical(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사회과학대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사회과학대학", category_type = "의료") | Benefit.objects.filter(end_date = None, category_univ = "사회과학대학", category_type = "의료") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "사회과학대학", category_type = "의료").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "사회과학대학", category_type = "의료") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#AI융합대학
#AI융합대학 전체게시물
def ai(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "AI융합대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "AI융합대학") | Benefit.objects.filter(end_date = None, category_univ = "AI융합대학") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "AI융합대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "AI융합대학") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#AI융합대학 식당 게시물
def ai_restaurant(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "AI융합대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "AI융합대학", category_type = "식당") | Benefit.objects.filter(end_date = None, category_univ = "AI융합대학", category_type = "식당") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "AI융합대학", category_type = "식당").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "AI융합대학", category_type = "식당") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#AI융합대학 주점 게시물
def ai_pub(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "AI융합대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "AI융합대학", category_type = "주점") | Benefit.objects.filter(end_date = None, category_univ = "AI융합대학", category_type = "주점") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "AI융합대학", category_type = "주점").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "AI융합대학", category_type = "주점") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#AI융합대학 카페 게시물
def ai_cafe(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "AI융합대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "AI융합대학", category_type = "카페") | Benefit.objects.filter(end_date = None, category_univ = "AI융합대학", category_type = "카페") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "AI융합대학", category_type = "카페").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "AI융합대학", category_type = "카페") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#AI융합대학 교육 게시물
def ai_education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "AI융합대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "AI융합대학", category_type = "교육") | Benefit.objects.filter(end_date = None, category_univ = "AI융합대학", category_type = "교육") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "AI융합대학", category_type = "교육").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "AI융합대학", category_type = "교육") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#AI융합대학 의료 게시물
def ai_medical(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "AI융합대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "AI융합대학", category_type = "의료") | Benefit.objects.filter(end_date = None, category_univ = "AI융합대학", category_type = "의료") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "AI융합대학", category_type = "의료").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "AI융합대학", category_type = "의료") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })


#공과대학
#공과대학 전체 게시물
def engineering(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "공과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "공과대학") | Benefit.objects.filter(end_date = None, category_univ = "공과대학") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "공과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "공과대학") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#공과대학 식당 게시물
def engineering_restaurant(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "공과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "공과대학", category_type = "식당") | Benefit.objects.filter(end_date = None, category_univ = "공과대학", category_type = "식당") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "공과대학", category_type = "식당").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "공과대학", category_type = "식당") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#공과대학 주점 게시물
def engineering_pub(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "공과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "공과대학", category_type = "주점") | Benefit.objects.filter(end_date = None, category_univ = "공과대학", category_type = "주점") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "공과대학", category_type = "주점").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "공과대학", category_type = "주점") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#공과대학 카페 게시물
def engineering_cafe(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "공과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "공과대학", category_type = "카페") | Benefit.objects.filter(end_date = None, category_univ = "공과대학", category_type = "카페") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "공과대학", category_type = "카페").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "공과대학", category_type = "카페") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#공과대학 교육 게시물
def engineering_education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "공과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "공과대학", category_type = "교육") | Benefit.objects.filter(end_date = None, category_univ = "공과대학", category_type = "교육") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "공과대학", category_type = "교육").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "공과대학", category_type = "교육") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#공과대학 의료 게시물
def engineering_medical(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "공과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "공과대학", category_type = "의료") | Benefit.objects.filter(end_date = None, category_univ = "공과대학", category_type = "의료") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "공과대학", category_type = "의료").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "공과대학", category_type = "의료") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#불교대학
#불교대학 전체 게시물
def buddhism(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "불교대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "불교대학") | Benefit.objects.filter(end_date = None, category_univ = "불교대학") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "불교대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "불교대학") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#불교대학 식당 게시물
def buddhism_restaurant(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "불교대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "불교대학", category_type = "식당") | Benefit.objects.filter(end_date = None, category_univ = "불교대학", category_type = "식당") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "불교대학", category_type = "식당").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "불교대학", category_type = "식당") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#불교대학 주점 게시물
def buddhism_pub(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "불교대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "불교대학", category_type = "주점") | Benefit.objects.filter(end_date = None, category_univ = "불교대학", category_type = "주점") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "불교대학", category_type = "주점").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "불교대학", category_type = "주점") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#불교대학 카페 게시물
def buddhism_cafe(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "불교대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "불교대학", category_type = "카페") | Benefit.objects.filter(end_date = None, category_univ = "불교대학", category_type = "카페") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "불교대학", category_type = "카페").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "불교대학", category_type = "카페") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#불교대학 교육 게시물
def buddhism_education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "불교대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "불교대학", category_type = "교육") | Benefit.objects.filter(end_date = None, category_univ = "불교대학", category_type = "교육") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "불교대학", category_type = "교육").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "불교대학", category_type = "교육") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#불교대학 의료 게시물
def buddhism_medical(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "불교대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "불교대학", category_type = "의료") | Benefit.objects.filter(end_date = None, category_univ = "불교대학", category_type = "의료") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "불교대학", category_type = "의료").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "불교대학", category_type = "의료") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#미래융합대학
#미래융합대학 전체 게시물
def future(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "미래융합대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "미래융합대학") | Benefit.objects.filter(end_date = None, category_univ = "미래융합대학") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "미래융합대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "미래융합대학") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#미래융합대학 식당 게시물
def future_restaurant(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "미래융합대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "미래융합대학", category_type = "식당") | Benefit.objects.filter(end_date = None, category_univ = "미래융합대학", category_type = "식당") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "미래융합대학", category_type = "식당").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "미래융합대학", category_type = "식당") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#미래융합대학 주점 게시물
def future_pub(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "미래융합대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "미래융합대학", category_type = "주점") | Benefit.objects.filter(end_date = None, category_univ = "미래융합대학", category_type = "주점") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "미래융합대학", category_type = "주점").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "미래융합대학", category_type = "주점") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#미래융합대학 카페 게시물
def future_cafe(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "미래융합대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "미래융합대학", category_type = "카페") | Benefit.objects.filter(end_date = None, category_univ = "미래융합대학", category_type = "카페") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "미래융합대학", category_type = "카페").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "미래융합대학", category_type = "카페") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#미래융합대학 교육 게시물
def future_education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "미래융합대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "미래융합대학", category_type = "교육") | Benefit.objects.filter(end_date = None, category_univ = "미래융합대학", category_type = "교육") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "미래융합대학", category_type = "교육").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "미래융합대학", category_type = "교육") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#미래융합대학 의료 게시물
def future_medical(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "미래융합대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "미래융합대학", category_type = "의료") | Benefit.objects.filter(end_date = None, category_univ = "미래융합대학", category_type = "의료") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "미래융합대학", category_type = "의료").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "미래융합대학", category_type = "의료") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#이과대학
#이과대학 전체 게시물
def science(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "이과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "이과대학") | Benefit.objects.filter(end_date = None, category_univ = "이과대학") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "이과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "이과대학") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#이과대학 식당 게시물
def science_restaurant(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "이과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "이과대학", category_type = "식당") | Benefit.objects.filter(end_date = None, category_univ = "이과대학", category_type = "식당") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "이과대학", category_type = "식당").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "이과대학", category_type = "식당") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#이과대학 주점 게시물
def science_pub(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "이과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "이과대학", category_type = "주점") | Benefit.objects.filter(end_date = None, category_univ = "이과대학", category_type = "주점") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "이과대학", category_type = "주점").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "이과대학", category_type = "주점") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#이과대학 카페 게시물
def science_cafe(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "이과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "이과대학", category_type = "카페") | Benefit.objects.filter(end_date = None, category_univ = "이과대학", category_type = "카페") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "이과대학", category_type = "카페").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "이과대학", category_type = "카페") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#이과대학 교육 게시물
def science_education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "이과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "이과대학", category_type = "교육") | Benefit.objects.filter(end_date = None, category_univ = "이과대학", category_type = "교육") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "이과대학", category_type = "교육").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "이과대학", category_type = "교육") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#이과대학 의료 게시물
def science_medical(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "이과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "이과대학", category_type = "의료") | Benefit.objects.filter(end_date = None, category_univ = "이과대학", category_type = "의료") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "이과대학", category_type = "의료").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "이과대학", category_type = "의료") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#문과대학
#문과대학 전체 게시물
def liberal(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "문과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "문과대학") | Benefit.objects.filter(end_date = None, category_univ = "문과대학") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "문과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "문과대학") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#문과대학 식당 게시물
def liberal_restaurant(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "문과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "문과대학", category_type = "식당") | Benefit.objects.filter(end_date = None, category_univ = "문과대학", category_type = "식당") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "문과대학", category_type = "식당").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "문과대학", category_type = "식당") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#문과대학 주점 게시물
def liberal_pub(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "문과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "문과대학", category_type = "주점") | Benefit.objects.filter(end_date = None, category_univ = "문과대학", category_type = "주점") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "문과대학", category_type = "주점").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "문과대학", category_type = "주점") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#문과대학 카페 게시물
def liberal_cafe(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "문과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "문과대학", category_type = "카페") | Benefit.objects.filter(end_date = None, category_univ = "문과대학", category_type = "카페") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "문과대학", category_type = "카페").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "문과대학", category_type = "카페") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#문과대학 교육 게시물
def liberal_education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "문과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "문과대학", category_type = "교육") | Benefit.objects.filter(end_date = None, category_univ = "문과대학", category_type = "교육") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "문과대학", category_type = "교육").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "문과대학", category_type = "교육") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#문과대학 의료 게시물
def liberal_medical(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "문과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "문과대학", category_type = "의료") | Benefit.objects.filter(end_date = None, category_univ = "문과대학", category_type = "의료") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "문과대학", category_type = "의료").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "문과대학", category_type = "의료") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#경찰사법대학
#경찰사법대학 전체 게시물
def police(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경찰사법대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경찰사법대학") | Benefit.objects.filter(end_date = None, category_univ = "경찰사법대학") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "경찰사법대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "경찰사법대학") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#경찰사법대학 식당 게시물
def police_restaurant(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경찰사법대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경찰사법대학", category_type = "식당") | Benefit.objects.filter(end_date = None, category_univ = "경찰사법대학", category_type = "식당") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "경찰사법대학", category_type = "식당").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "경찰사법대학", category_type = "식당") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#경찰사법대학 주점 게시물
def police_pub(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경찰사법대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경찰사법대학", category_type = "주점") | Benefit.objects.filter(end_date = None, category_univ = "경찰사법대학", category_type = "주점") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "경찰사법대학", category_type = "주점").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "경찰사법대학", category_type = "주점") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#경찰사법대학 카페 게시물
def police_cafe(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경찰사법대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경찰사법대학", category_type = "카페") | Benefit.objects.filter(end_date = None, category_univ = "경찰사법대학", category_type = "카페") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "경찰사법대학", category_type = "카페").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "경찰사법대학", category_type = "카페") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#경찰사법대학 교육 게시물
def police_education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경찰사법대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경찰사법대학", category_type = "교육") | Benefit.objects.filter(end_date = None, category_univ = "경찰사법대학", category_type = "교육") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "경찰사법대학", category_type = "교육").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "경찰사법대학", category_type = "교육") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#경찰사법대학 의료 게시물
def police_medical(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경찰사법대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경찰사법대학", category_type = "의료") | Benefit.objects.filter(end_date = None, category_univ = "경찰사법대학", category_type = "의료") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "경찰사법대학", category_type = "의료").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "경찰사법대학", category_type = "의료") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#사범대학
#사범대학 전체 게시물
def education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사범대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사범대학") | Benefit.objects.filter(end_date = None, category_univ = "사범대학") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "사범대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "사범대학") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#사범대학 식당 게시물
def education_restaurant(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사범대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사범대학", category_type = "식당") | Benefit.objects.filter(end_date = None, category_univ = "사범대학", category_type = "식당") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "사범대학", category_type = "식당").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "사범대학", category_type = "식당") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#사범대학 주점 게시물
def education_pub(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사범대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사범대학", category_type = "주점") | Benefit.objects.filter(end_date = None, category_univ = "사범대학", category_type = "주점") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "사범대학", category_type = "주점").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "사범대학", category_type = "주점") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#사범대학 카페 게시물
def education_cafe(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사범대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사범대학", category_type = "카페") | Benefit.objects.filter(end_date = None, category_univ = "사범대학", category_type = "카페") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "사범대학", category_type = "카페").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "사범대학", category_type = "카페") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#사범대학 교육 게시물
def education_education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사범대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사범대학", category_type = "교육") | Benefit.objects.filter(end_date = None, category_univ = "사범대학", category_type = "교육") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "사범대학", category_type = "교육").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "사범대학", category_type = "교육") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#사범대학 의료 게시물
def education_medical(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사범대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사범대학", category_type = "의료") | Benefit.objects.filter(end_date = None, category_univ = "사범대학", category_type = "의료") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "사범대학", category_type = "의료").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "사범대학", category_type = "의료") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#법과대학
#법과대학 전체 게시물
def law(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "법과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "법과대학") | Benefit.objects.filter(end_date = None, category_univ = "법과대학") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "법과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "법과대학") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#법과대학 식당 게시물
def law_restaurant(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "법과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "법과대학", category_type = "식당") | Benefit.objects.filter(end_date = None, category_univ = "법과대학", category_type = "식당") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "법과대학", category_type = "식당").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "법과대학", category_type = "식당") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#법과대학 주점 게시물
def law_pub(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "법과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "법과대학", category_type = "주점") | Benefit.objects.filter(end_date = None, category_univ = "법과대학", category_type = "주점") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "법과대학", category_type = "주점").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "법과대학", category_type = "주점") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#법과대학 카페 게시물
def law_cafe(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "법과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "법과대학", category_type = "카페") | Benefit.objects.filter(end_date = None, category_univ = "법과대학", category_type = "카페") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "법과대학", category_type = "카페").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "법과대학", category_type = "카페") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#법과대학 교육 게시물
def law_education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "법과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "법과대학", category_type = "교육") | Benefit.objects.filter(end_date = None, category_univ = "법과대학", category_type = "교육") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "법과대학", category_type = "교육").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "법과대학", category_type = "교육") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

#법과대학 의료 게시물
def law_medical(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "법과대학"
    posts = Benefit.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "법과대학", category_type = "의료") | Benefit.objects.filter(end_date = None, category_univ = "법과대학", category_type = "의료") | Benefit.objects.filter(start_date = None, end_date__gte = now, category_univ = "법과대학", category_type = "의료").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(end_date__lt = now, category_univ = "법과대학", category_type = "의료") #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 두번 째 줄부터 채움. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_second_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_first_line.append(end_post) #담아담아
    else:
        for i, end_post in enumerate(end_posts):
            if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
                end_first_line.append(end_post)
            elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
                end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'univ' : univ,
        'post_first_line' : post_first_line,
        'post_second_line' : post_second_line,
        'end_first_line' : end_first_line,
        'end_second_line' : end_second_line,
        })

def create(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                new_benefit = Benefit()

                new_benefit.title = request.POST['title']
                new_benefit.writer = request.user
                new_benefit.pub_date = timezone.now()
                new_benefit.category_univ = request.POST['category_univ']
                new_benefit.category_type = request.POST['category_type']
                if request.POST['start_time']:
                    new_benefit.start_time = request.POST['start_time']
                if request.POST['end_time']:
                    new_benefit.end_time = request.POST['end_time']
                new_benefit.address = request.POST['address']
                if request.POST['start_date']:
                    new_benefit.start_date = request.POST['start_date']
                if request.POST['end_date']:
                    new_benefit.end_date = request.POST['end_date']
                new_benefit.image = request.FILES.get('image')
                new_benefit.body = request.POST['body']

                new_benefit.save()
                
                return redirect('benefits:detail', new_benefit.id)
            
            elif request.method == 'GET':
                return render(request, 'benefits/new.html')
            
        else:
            return render(request, 'accounts/no_auth.html')
    else:
        return redirect('accounts:login')

def detail(request, benefit_id):
    benefit = get_object_or_404(Benefit, pk = benefit_id)
    comments = BComment.objects.filter(benefit = benefit)
    comments_count = len(comments)
    return render(request, 'benefits/detail.html',{
        'benefit' : benefit,
        'comments' : comments,
        'comments_count' : comments_count,
        })

def review(request, benefit_id):#댓글 작성하는 칸
    if request.user.is_authenticated:
        benefit = Benefit.objects.get(id = benefit_id) #게시물 id에 맞는 게시물을 담음
        if request.method == 'POST':
            new_comment = BComment() #댓글 빈 객체 생성
            new_comment.benefit = benefit #게시물 비교하기 위한 공간에 이 게시물 담음
            new_comment.writer = request.user
            new_comment.content = request.POST['content'] #댓글 내용 담아담아
            new_comment.benefit_rate = request.POST['benefit_rate'] #평점 담아담아
            new_comment.pub_date = timezone.now() #댓글 작성한 시간 담아담아

            new_comment.save() #댓글 저장, id 생성
        
            return redirect('benefits:detail', benefit.id)
    
        elif request.method == 'GET':
            benefit = Benefit.objects.get(id = benefit_id)
            comments = BComment.objects.filter(benefit = benefit)
            comments_count = len(comments)
            return render(request, 'benefits/review.html',{
                'benefit' : benefit,
                'comments' : comments,
                'comments_count' : comments_count,
                })
    else:
        return redirect('accounts:login')
    
def comment_likes(request, comment_id):
    if request.user.is_authenticated: 
        comment = get_object_or_404(BComment, id=comment_id)
        if request.user in comment.comment_like.all():
            comment.comment_like.remove(request.user)
            comment.comment_like_count -=1
            comment.save()
        else:
            comment.comment_like.add(request.user)
            comment.comment_like_count +=1
            comment.save()
        return redirect('benefits:detail', comment.benefit.id)
    else:
        return render(request, 'accounts/no_auth.html')


def delete_comment(request, comment_id):
    delete_comment = BComment.objects.get(id = comment_id)
    if request.user == delete_comment.writer:
        delete_comment.delete()
        return redirect('benefits:detail', delete_comment.benefit.id)
    elif request.user.is_superuser:
        delete_comment.delete()
        return redirect('benefits:detail', delete_comment.benefit.id)
    else:
        return render(request, 'accounts/no_auth.html')

def edit_comment(request, comment_id):
    if request.user.is_authenticated:
        edit_comment = get_object_or_404(BComment, pk=comment_id)
        if request.user == edit_comment.writer:
            if request.method == 'POST':
                edit_comment.benefit = edit_comment.benefit #게시물 비교하기 위한 공간에 이 게시물 담음
                edit_comment.writer = request.user
                edit_comment.content = request.POST['content'] #댓글 내용 담아담아
                edit_comment.benefit_rate = request.POST['benefit_rate'] #평점 담아담아
                edit_comment.pub_date = timezone.now() #댓글 작성한 시간 담아담아

                edit_comment.save() #댓글 저장, id 생성
            
                return redirect('benefits:detail', edit_comment.benefit.id)
            elif request.method == 'GET':
                benefit = Benefit.objects.get(id = edit_comment.benefit.id)
                comments = BComment.objects.filter(benefit = benefit)
                comments_count = len(comments)
                return render(request, 'benefits/edit_comment.html',{
                    'comment' : edit_comment,
                    'benefit' : benefit,
                    'comments' : comments,
                    'comments_count' : comments_count,
                    })
        elif request.user.is_superuser:
            if request.method == 'POST':
                edit_comment.benefit = edit_comment.benefit #게시물 비교하기 위한 공간에 이 게시물 담음
                edit_comment.writer = request.user
                edit_comment.content = request.POST['content'] #댓글 내용 담아담아
                edit_comment.benefit_rate = request.POST['benefit_rate'] #평점 담아담아
                edit_comment.pub_date = timezone.now() #댓글 작성한 시간 담아담아

                edit_comment.save() #댓글 저장, id 생성
            
                return redirect('benefits:detail', edit_comment.benefit.id)
            elif request.method == 'GET':
                benefit = Benefit.objects.get(id = edit_comment.benefit.id)
                comments = BComment.objects.filter(benefit = benefit)
                comments_count = len(comments)
                return render(request, 'benefits/edit_comment.html',{
                    'comment' : edit_comment,
                    'benefit' : benefit,
                    'comments' : comments,
                    'comments_count' : comments_count,
                    })
        else:
            return render(request, 'accounts/no_auth.html')
    else:
        return redirect('accounts:login')

def update(request, benefit_id):
    if request.user.is_staff:
        update_benefit = Benefit.objects.get(id = benefit_id)
        if request.user == update_benefit.writer:
            if request.method == 'POST':
                update_benefit.title = request.POST['title']
                update_benefit.writer = request.user
                update_benefit.pub_date = timezone.now()
                if request.POST['start_time']:
                    update_benefit.start_time = request.POST['start_time']
                if request.POST['end_time']:
                    update_benefit.end_time = request.POST['end_time']
                update_benefit.address = request.POST['address']
                if request.POST['start_date']:
                    update_benefit.start_date = request.POST['start_date']
                if request.POST['end_date']:
                    update_benefit.end_date = request.POST['end_date']
                update_benefit.image = request.FILES.get('image', update_benefit.image)
                update_benefit.body = request.POST['body']

                update_benefit.save()

                return redirect('benefits:detail', update_benefit.id)
            
            elif request.method == 'GET':
                edit_benefit = Benefit.objects.get(id = benefit_id)
                return render(request, 'benefits/edit.html', {
                    'benefit' : edit_benefit,
                    })
        elif request.user.is_superuser:
            if request.method == 'POST':
                update_benefit.title = request.POST['title']
                update_benefit.writer = request.user
                if request.POST['start_time']:
                    update_benefit.start_time = request.POST['start_time']
                if request.POST['end_time']:
                    update_benefit.end_time = request.POST['end_time']
                update_benefit.address = request.POST['address']
                if request.POST['start_date']:
                    update_benefit.start_date = request.POST['start_date']
                if request.POST['end_date']:
                    update_benefit.end_date = request.POST['end_date']
                update_benefit.image = request.FILES.get('image', update_benefit.image)
                update_benefit.body = request.POST['body']

                update_benefit.save()

                return redirect('benefits:detail', update_benefit.id)
            
            elif request.method == 'GET':
                edit_benefit = Benefit.objects.get(id = benefit_id)
                return render(request, 'benefits/edit.html', {
                    'benefit':edit_benefit,
                    })
        else:
            return render(request, 'accounts/no_auth.html')
    else:
        return render(request, 'accounts/no_auth.html')

def delete(request, benefit_id):
    if request.user.is_staff:
        delete_benefits = Benefit.objects.get(id = benefit_id)
        if request.user == delete_benefits.writer:
            delete_benefits.delete()
            return redirect('benefits:choose')
        elif request.user.is_superuser:
            delete_benefits.delete()
            return redirect('benefits:choose')
        else:
            return render(request, 'accounts/no_auth.html')
    else:
        return render(request, 'accounts/no_auth.html')

def benefit_like_toggle(request):
    if request.user.is_authenticated: #유저가 로그인했으면
        pk = request.GET["pk"]
        benefit = get_object_or_404(Benefit, pk=pk) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in benefit.benefit_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            benefit.benefit_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            benefit.benefit_like_count -=1 # 좋아요 개수 1개 줄음
            benefit.save() #저장
            result = "like_cancel"
        else:
            benefit.benefit_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            benefit.benefit_like_count +=1 #좋아요 1개 추가
            benefit.save()
            result = "like"

        context = {
            "benefit_like_count" : benefit.benefit_like_count,
            "result" : result
        }

        return HttpResponse(json.dumps(context), content_type = "application/json")
    else:
        return render(request, 'accounts/no_auth.html')
    
def comment_like_toggle(request):
    if request.user.is_authenticated: #유저가 로그인했으면
        pk = request.GET["pk"]
        comment = get_object_or_404(BComment, pk=pk) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in comment.comment_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            comment.comment_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            comment.comment_like_count -=1 # 좋아요 개수 1개 줄음
            comment.save() #저장
            result = "like_cancel"
        else:
            comment.comment_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            comment.comment_like_count +=1 #좋아요 1개 추가
            comment.save()
            result = "like"

        context = {
            "comment_like_count" : comment.comment_like_count,
            "result" : result
        }

        return HttpResponse(json.dumps(context), content_type = "application/json")
    else:
        return render(request, 'accounts/no_auth.html')


def detail_likes(request, benefit_id): # 게시물 안에서 좋아요 누를 때
    if request.user.is_authenticated: #위와 동일
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
