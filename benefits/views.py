from django.shortcuts import render, redirect, get_object_or_404
from .models import Benefit, BComment
from accounts.models import CustomUser
from django.utils import timezone


def choose(request):
    return render(request, 'benefits/choose.html')

# 각 단과대학 게시물 뜨게 하는 함수
# 경영대학
def business(request):
    now = timezone.now() #현재 시간 받아옴
    posts = Benefit.objects.filter(start_date__lt = now, end_date__gt = now, category_univ = "경영대학").order_by('end_date') #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
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

    return render(request, 'benefits/business.html', {
        'post_first_line':post_first_line,
        'post_second_line':post_second_line,
        'end_first_line':end_first_line,
        'end_second_line':end_second_line,
        })

#예술 대학
def art(request):
    now = timezone.now() #현재 시간 받아옴
    posts = Benefit.objects.filter(start_date__lt = now, end_date__gt = now, category_univ = "예술대학").order_by('end_date') #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
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

    return render(request, 'benefits/art.html', {
        'post_first_line':post_first_line,
        'post_second_line':post_second_line,
        'end_first_line':end_first_line,
        'end_second_line':end_second_line,
        })

#사회과학대학
def social(request):
    now = timezone.now() #현재 시간 받아옴
    posts = Benefit.objects.filter(start_date__lt = now, end_date__gt = now, category_univ = "사회과학대학").order_by('end_date') #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
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

    return render(request, 'benefits/social.html', {
        'post_first_line':post_first_line,
        'post_second_line':post_second_line,
        'end_first_line':end_first_line,
        'end_second_line':end_second_line,
        })

#AI융합대학
def ai(request):
    now = timezone.now() #현재 시간 받아옴
    posts = Benefit.objects.filter(start_date__lt = now, end_date__gt = now, category_univ = "AI융합대학").order_by('end_date') #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
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

    return render(request, 'benefits/ai.html', {
        'post_first_line':post_first_line,
        'post_second_line':post_second_line,
        'end_first_line':end_first_line,
        'end_second_line':end_second_line,
        })

#공과대학
def engineering(request):
    now = timezone.now() #현재 시간 받아옴
    posts = Benefit.objects.filter(start_date__lt = now, end_date__gt = now, category_univ = "공과대학").order_by('end_date') #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
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

    return render(request, 'benefits/engineering.html', {
        'post_first_line':post_first_line,
        'post_second_line':post_second_line,
        'end_first_line':end_first_line,
        'end_second_line':end_second_line,
        })

#불교대학
def buddhism(request):
    now = timezone.now() #현재 시간 받아옴
    posts = Benefit.objects.filter(start_date__lt = now, end_date__gt = now, category_univ = "불교대학").order_by('end_date') #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
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

    return render(request, 'benefits/buddhism.html', {
        'post_first_line':post_first_line,
        'post_second_line':post_second_line,
        'end_first_line':end_first_line,
        'end_second_line':end_second_line,
        })

#미래융합대학
def future(request):
    now = timezone.now() #현재 시간 받아옴
    posts = Benefit.objects.filter(start_date__lt = now, end_date__gt = now, category_univ = "미래융합대학").order_by('end_date') #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
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

    return render(request, 'benefits/future.html', {
        'post_first_line':post_first_line,
        'post_second_line':post_second_line,
        'end_first_line':end_first_line,
        'end_second_line':end_second_line,
        })

#이과대학
def science(request):
    now = timezone.now() #현재 시간 받아옴
    posts = Benefit.objects.filter(start_date__lt = now, end_date__gt = now, category_univ = "이과대학").order_by('end_date') #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
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

    return render(request, 'benefits/science.html', {
        'post_first_line':post_first_line,
        'post_second_line':post_second_line,
        'end_first_line':end_first_line,
        'end_second_line':end_second_line,
        })

#문과대학
def liberal(request):
    now = timezone.now() #현재 시간 받아옴
    posts = Benefit.objects.filter(start_date__lt = now, end_date__gt = now, category_univ = "문과대학").order_by('end_date') #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
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

    return render(request, 'benefits/liberal.html', {
        'post_first_line':post_first_line,
        'post_second_line':post_second_line,
        'end_first_line':end_first_line,
        'end_second_line':end_second_line,
        })

#경찰사법대학
def police(request):
    now = timezone.now() #현재 시간 받아옴
    posts = Benefit.objects.filter(start_date__lt = now, end_date__gt = now, category_univ = "경찰사법대학").order_by('end_date') #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
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

    return render(request, 'benefits/police.html', {
        'post_first_line':post_first_line,
        'post_second_line':post_second_line,
        'end_first_line':end_first_line,
        'end_second_line':end_second_line,
        })

#사범대학
def education(request):
    now = timezone.now() #현재 시간 받아옴
    posts = Benefit.objects.filter(start_date__lt = now, end_date__gt = now, category_univ = "사범대학").order_by('end_date') #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
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

    return render(request, 'benefits/education.html', {
        'post_first_line':post_first_line,
        'post_second_line':post_second_line,
        'end_first_line':end_first_line,
        'end_second_line':end_second_line,
        })

#법과대학
def law(request):
    now = timezone.now() #현재 시간 받아옴
    posts = Benefit.objects.filter(start_date__lt = now, end_date__gt = now, category_univ = "법과대학").order_by('end_date') #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
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

    return render(request, 'benefits/law.html', {
        'post_first_line':post_first_line,
        'post_second_line':post_second_line,
        'end_first_line':end_first_line,
        'end_second_line':end_second_line,
        })

def create(request):
    if request.user.is_authenticated:
        new_benefit = Benefit()
        new_benefit.title = request.POST['title']
        new_benefit.writer = request.user
        new_benefit.category_univ = request.POST['category_univ']
        new_benefit.category_type = request.POST['category_type']
        new_benefit.start_time = request.POST['start_time']
        new_benefit.end_time = request.POST['end_time']
        new_benefit.address = request.POST['address']
        new_benefit.start_date = request.POST['start_date']
        new_benefit.end_date = request.POST['end_date']
        new_benefit.image = request.FILES.get('image')
        new_benefit.body = request.POST['body']

        new_benefit.save()
        
        return redirect('benefits:detail', new_benefit.id)
    else:
        return redirect('accounts:login')

def new(request):
    return render(request, 'benefits/new.html')

def detail(request, id):
    benefit = get_object_or_404(Benefit, pk = id)
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
    else:
        return redirect('accounts:login')
    
    if request.method == 'GET':
        benefit = Benefit.objects.get(id = benefit_id)
        comments = BComment.objects.filter(benefit = benefit)
        comments_count = len(comments)
        return render(request, 'benefits/review.html',{
            'benefit':benefit,
            'comments' : comments,
            'comments_count' : comments_count,
            })
    
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
    delete_comment.delete()
    return redirect('benefits:detail', delete_comment.benefit.id)
    
def edit_comment(request, comment_id):
    edit_comment = BComment.objects.get(id = comment_id)
    benefit = Benefit.objects.get(id = edit_comment.benefit.id)
    comments = BComment.objects.filter(benefit = benefit)
    comments_count = len(comments)
    return render(request, 'benefits/edit_comment.html',{
        'edit_comment':edit_comment,
        'benefit':benefit,
        'comments' : comments,
        'comments_count' : comments_count,
        })

def edit_comment(request, comment_id):
    if request.user.is_authenticated:
        edit_comment = get_object_or_404(BComment, pk=comment_id)
        if request.method == 'POST':
            edit_comment.benefit = edit_comment.benefit #게시물 비교하기 위한 공간에 이 게시물 담음
            edit_comment.writer = request.user
            edit_comment.content = request.POST['content'] #댓글 내용 담아담아
            edit_comment.benefit_rate = request.POST['benefit_rate'] #평점 담아담아
            edit_comment.pub_date = timezone.now() #댓글 작성한 시간 담아담아

            edit_comment.save() #댓글 저장, id 생성
        
            return redirect('benefits:detail', edit_comment.benefit.id)
        if request.method == 'GET':
            benefit = Benefit.objects.get(id = edit_comment.benefit.id)
            comments = BComment.objects.filter(benefit = benefit)
            comments_count = len(comments)
            return render(request, 'benefits/edit_comment.html',{
                'comment':edit_comment,
                'benefit':benefit,
                'comments' : comments,
                'comments_count' : comments_count,
                })
    else:
        return redirect('accounts:login')

def edit(request, id):
    edit_benefit = Benefit.objects.get(id = id)
    return render(request, 'benefits/edit.html', {
        'benefit':edit_benefit,
    })

def update(request, id):
    if request.user.is_authenticated:
        update_benefit = Benefit.objects.get(id = id)
        if request.user == update_benefit.writer:
            update_benefit.title = request.POST['title']
            update_benefit.writer = request.user
            update_benefit.start_date = request.POST['start_date']
            update_benefit.due_date = request.POST['due_date']
            update_benefit.image = request.FILES.get('image', update_benefit.image)
            update_benefit.body = request.POST['body']

            update_benefit.save()

            return redirect('benefits:detail', update_benefit.id)
    else:
        return redirect('accounts:login')

def delete(request, id):
    delete_benefits = Benefit.objects.get(id = id)
    delete_benefits.delete()
    return redirect('benefits:choose')

#경영대학 메인페이지 좋아요
def business_likes(request, benefit_id): #메인 페이지에서 좋아요 누를 때
    if request.user.is_authenticated: #유저가 로그인했으면
        benefit = get_object_or_404(Benefit, id=benefit_id) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in benefit.benefit_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            benefit.benefit_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            benefit.benefit_like_count -=1 # 좋아요 개수 1개 줄음
            benefit.save() #저장
        else:
            benefit.benefit_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            benefit.benefit_like_count +=1 #좋아요 1개 추가
            benefit.save()
        return redirect('benefits:business')
    else:
        return render(request, 'accounts/no_auth.html')
    
#예술대학 메인페이지 좋아요
def art_likes(request, benefit_id): #메인 페이지에서 좋아요 누를 때
    if request.user.is_authenticated: #유저가 로그인했으면
        benefit = get_object_or_404(Benefit, id=benefit_id) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in benefit.benefit_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            benefit.benefit_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            benefit.benefit_like_count -=1 # 좋아요 개수 1개 줄음
            benefit.save() #저장
        else:
            benefit.benefit_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            benefit.benefit_like_count +=1 #좋아요 1개 추가
            benefit.save()
        return redirect('benefits:art')
    else:
        return render(request, 'accounts/no_auth.html')
    
#사회과학대학 메인페이지 좋아요
def social_likes(request, benefit_id): #메인 페이지에서 좋아요 누를 때
    if request.user.is_authenticated: #유저가 로그인했으면
        benefit = get_object_or_404(Benefit, id=benefit_id) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in benefit.benefit_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            benefit.benefit_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            benefit.benefit_like_count -=1 # 좋아요 개수 1개 줄음
            benefit.save() #저장
        else:
            benefit.benefit_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            benefit.benefit_like_count +=1 #좋아요 1개 추가
            benefit.save()
        return redirect('benefits:social')
    else:
        return render(request, 'accounts/no_auth.html')
    
#AI융합대학 메인페이지 좋아요
def ai_likes(request, benefit_id): #메인 페이지에서 좋아요 누를 때
    if request.user.is_authenticated: #유저가 로그인했으면
        benefit = get_object_or_404(Benefit, id=benefit_id) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in benefit.benefit_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            benefit.benefit_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            benefit.benefit_like_count -=1 # 좋아요 개수 1개 줄음
            benefit.save() #저장
        else:
            benefit.benefit_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            benefit.benefit_like_count +=1 #좋아요 1개 추가
            benefit.save()
        return redirect('benefits:ai')
    else:
        return render(request, 'accounts/no_auth.html')
    
#공과대학 메인페이지 좋아요
def engineering_likes(request, benefit_id): #메인 페이지에서 좋아요 누를 때
    if request.user.is_authenticated: #유저가 로그인했으면
        benefit = get_object_or_404(Benefit, id=benefit_id) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in benefit.benefit_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            benefit.benefit_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            benefit.benefit_like_count -=1 # 좋아요 개수 1개 줄음
            benefit.save() #저장
        else:
            benefit.benefit_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            benefit.benefit_like_count +=1 #좋아요 1개 추가
            benefit.save()
        return redirect('benefits:engineering')
    else:
        return render(request, 'accounts/no_auth.html')
    
#불교대학 메인페이지 좋아요
def buddhism_likes(request, benefit_id): #메인 페이지에서 좋아요 누를 때
    if request.user.is_authenticated: #유저가 로그인했으면
        benefit = get_object_or_404(Benefit, id=benefit_id) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in benefit.benefit_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            benefit.benefit_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            benefit.benefit_like_count -=1 # 좋아요 개수 1개 줄음
            benefit.save() #저장
        else:
            benefit.benefit_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            benefit.benefit_like_count +=1 #좋아요 1개 추가
            benefit.save()
        return redirect('benefits:buddhism')
    else:
        return render(request, 'accounts/no_auth.html')
    
#미래융합대학 메인페이지 좋아요
def future_likes(request, benefit_id): #메인 페이지에서 좋아요 누를 때
    if request.user.is_authenticated: #유저가 로그인했으면
        benefit = get_object_or_404(Benefit, id=benefit_id) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in benefit.benefit_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            benefit.benefit_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            benefit.benefit_like_count -=1 # 좋아요 개수 1개 줄음
            benefit.save() #저장
        else:
            benefit.benefit_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            benefit.benefit_like_count +=1 #좋아요 1개 추가
            benefit.save()
        return redirect('benefits:future')
    else:
        return render(request, 'accounts/no_auth.html')
    
#이과대학 메인페이지 좋아요
def science_likes(request, benefit_id): #메인 페이지에서 좋아요 누를 때
    if request.user.is_authenticated: #유저가 로그인했으면
        benefit = get_object_or_404(Benefit, id=benefit_id) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in benefit.benefit_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            benefit.benefit_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            benefit.benefit_like_count -=1 # 좋아요 개수 1개 줄음
            benefit.save() #저장
        else:
            benefit.benefit_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            benefit.benefit_like_count +=1 #좋아요 1개 추가
            benefit.save()
        return redirect('benefits:science')
    else:
        return render(request, 'accounts/no_auth.html')
    
#문과대학 메인페이지 좋아요
def liberal_likes(request, benefit_id): #메인 페이지에서 좋아요 누를 때
    if request.user.is_authenticated: #유저가 로그인했으면
        benefit = get_object_or_404(Benefit, id=benefit_id) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in benefit.benefit_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            benefit.benefit_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            benefit.benefit_like_count -=1 # 좋아요 개수 1개 줄음
            benefit.save() #저장
        else:
            benefit.benefit_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            benefit.benefit_like_count +=1 #좋아요 1개 추가
            benefit.save()
        return redirect('benefits:liberal')
    else:
        return render(request, 'accounts/no_auth.html')
    
#경찰사법대학 메인페이지 좋아요
def police_likes(request, benefit_id): #메인 페이지에서 좋아요 누를 때
    if request.user.is_authenticated: #유저가 로그인했으면
        benefit = get_object_or_404(Benefit, id=benefit_id) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in benefit.benefit_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            benefit.benefit_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            benefit.benefit_like_count -=1 # 좋아요 개수 1개 줄음
            benefit.save() #저장
        else:
            benefit.benefit_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            benefit.benefit_like_count +=1 #좋아요 1개 추가
            benefit.save()
        return redirect('benefits:police')
    else:
        return render(request, 'accounts/no_auth.html')
    
#사범대학 메인페이지 좋아요
def education_likes(request, benefit_id): #메인 페이지에서 좋아요 누를 때
    if request.user.is_authenticated: #유저가 로그인했으면
        benefit = get_object_or_404(Benefit, id=benefit_id) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in benefit.benefit_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            benefit.benefit_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            benefit.benefit_like_count -=1 # 좋아요 개수 1개 줄음
            benefit.save() #저장
        else:
            benefit.benefit_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            benefit.benefit_like_count +=1 #좋아요 1개 추가
            benefit.save()
        return redirect('benefits:education')
    else:
        return render(request, 'accounts/no_auth.html')
    
#법과대학 메인페이지 좋아요
def law_likes(request, benefit_id): #메인 페이지에서 좋아요 누를 때
    if request.user.is_authenticated: #유저가 로그인했으면
        benefit = get_object_or_404(Benefit, id=benefit_id) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in benefit.benefit_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            benefit.benefit_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            benefit.benefit_like_count -=1 # 좋아요 개수 1개 줄음
            benefit.save() #저장
        else:
            benefit.benefit_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            benefit.benefit_like_count +=1 #좋아요 1개 추가
            benefit.save()
        return redirect('benefits:law')
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

