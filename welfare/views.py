from django.shortcuts import render, redirect, get_object_or_404
from .models import Welfare, WComment
from django.utils import timezone
from datetime import date


def mainpage(request):
    today = timezone.now()
    # 기간이 끝나지 않은 게시물
    welfares_notend = Welfare.objects.filter(start_date__lte = today, end_date__gte = today)
    first_rows_notend = []
    second_rows_notend = []
    # 기간이 끝난 게시물
    welfares_end = Welfare.objects.filter(end_date__lte = today)
    first_rows_end = []
    second_rows_end = []
    # 기간이 끝나지 않은 게시물
    for index, welfare_notend in enumerate(welfares_notend):
        if (index+1)%2 == 1:
            first_rows_notend.append(welfare_notend) # 짝수이면, first_rows에 담아
        else:
            second_rows_notend.append(welfare_notend) # 홀수이면, second_rows에 담아
    # 기간이 끝난 게시물
    for index, welfare_end in enumerate(welfares_end):
        # 만약 끝나지 않은 글 개수가 짝수면,
        if len(welfares_notend)%2 == 0:
            if (index+1)%2 == 1:
                first_rows_end.append(welfare_end) # 짝수이면, first_rows에 담아
            else:
                second_rows_end.append(welfare_end) # 홀수이면, second_rows에 담아
        # 만약 끝나지 않은 글 개수가 홀수면,
        else:
            if (index+1)%2 == 0:
                first_rows_end.append(welfare_end)
            else:
                second_rows_end.append(welfare_end)

    return render(request, 'welfare/mainpage.html', {
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def create(request):
    if request.user.is_authenticated:
        new_welfare = Welfare()
        new_welfare.title = request.POST['title']
        new_welfare.writer = request.user
        new_welfare.category_univ = request.POST['category_univ']
        new_welfare.category_type = request.POST['category_type']
        new_welfare.start_time = request.POST['start_time']
        new_welfare.end_time = request.POST['end_time']
        new_welfare.address = request.POST['address']
        new_welfare.start_date = request.POST['start_date']
        new_welfare.end_date = request.POST['end_date']
        new_welfare.image = request.FILES.get('image')
        new_welfare.body = request.POST['body']

        new_welfare.save()
        
        return redirect('welfare:detail', new_welfare.id)
    else:
        return redirect('accounts:login')

def new(request):
    return render(request, 'welfare/new.html')


def detail(request, id):
    welfare = get_object_or_404(Welfare, pk = id)
    comments = WComment.objects.filter(welfare = welfare)
    comments_count = len(comments)
    return render(request, 'welfare/detail.html',{
        'welfare':welfare,
        'comments' : comments,
        'comments_count' : comments_count,
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

def review(request, welfare_id): # 댓글 작성 함수
    if request.user.is_authenticated:
        welfare = Welfare.objects.get(id = welfare_id) # 게시물 id에 맞는 게시물을 담음
        if request.method == 'POST': # 댓글 작성작성
            new_comment = WComment() # 댓글 빈 객체 생성
            new_comment.welfare = welfare # 게시물 비교하기 위한 
            new_comment.writer = request.user
            new_comment.content = request.POST['content'] # 댓글 내용 담음
            new_comment.pub_date = timezone.now() # 댓글 작성한 시간 담음

            new_comment.save()

            return redirect('welfare:detail', welfare.id)
    else:
        return redirect('accounts:login')
    
    if request.method == 'GET': # 댓글 보기보기
        welfare = Welfare.objects.get(id = welfare_id) # 게시물 id에 맞는 게시물을 담음
        comments = WComment.objects.filter(welfare = welfare)
        comments_count = len(comments)
        return render(request, 'welfare/review.html',{
                'welfare':welfare,
                'comments' : comments,
                'comments_count' : comments_count,
                })

