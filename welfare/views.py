from django.shortcuts import render, redirect, get_object_or_404
from .models import Welfare, WComment
from django.utils import timezone
from datetime import date
from django.db.models import F
from accounts.models import CustomUser
from django.http import HttpResponse
import json


def choose(request):
    return render(request, 'welfare/choose.html')

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
        new_welfare.pub_date = timezone.now()
        new_welfare.category_univ = request.POST['category_univ']
        new_welfare.category_type = request.POST['category_type']
        if request.POST['start_time']:
            new_welfare.start_time = request.POST['start_time']
        if request.POST['end_time']:
            new_welfare.end_time = request.POST['end_time']
        new_welfare.address = request.POST['address']
        if request.POST['start_date']:
            new_welfare.start_date = request.POST['start_date']
        if request.POST['end_date']:
            new_welfare.end_date = request.POST['end_date']
        new_welfare.image = request.FILES.get('image')
        new_welfare.body = request.POST['body']

        new_welfare.save()
        
        return redirect('welfare:detail', new_welfare.id)
    else:
        return redirect('accounts:login')

def new(request):
    return render(request, 'welfare/new.html')

def update(request, welfare_id):
    if request.user.is_staff:
        update_welfare = Welfare.objects.get(id = welfare_id)
        if request.user == update_welfare.writer:
            if request.method == 'POST':
                update_welfare.title = request.POST['title']
                update_welfare.writer = request.user
                update_welfare.pub_date = timezone.now()
                if request.POST['start_time']:
                    update_welfare.start_time = request.POST['start_time']
                if request.POST['end_time']:
                    update_welfare.end_time = request.POST['end_time']
                update_welfare.address = request.POST['address']
                if request.POST['start_date']:
                    update_welfare.start_date = request.POST['start_date']
                if request.POST['end_date']:
                    update_welfare.end_date = request.POST['end_date']
                update_welfare.image = request.FILES.get('image', update_welfare.image)
                update_welfare.body = request.POST['body']

                update_welfare.save()

                return redirect('welfare:detail', update_welfare.id)
            
            elif request.method == 'GET':
                edit_welfare = Welfare.objects.get(id = welfare_id)
                return render(request, 'welfare/edit.html', {
                    'welfare' : edit_welfare,
                    })
        elif request.user.is_superuser:
            if request.method == 'POST':
                update_welfare.title = request.POST['title']
                update_welfare.writer = request.user
                if request.POST['start_time']:
                    update_welfare.start_time = request.POST['start_time']
                if request.POST['end_time']:
                    update_welfare.end_time = request.POST['end_time']
                update_welfare.address = request.POST['address']
                if request.POST['start_date']:
                    update_welfare.start_date = request.POST['start_date']
                if request.POST['end_date']:
                    update_welfare.end_date = request.POST['end_date']
                update_welfare.image = request.FILES.get('image', update_welfare.image)
                update_welfare.body = request.POST['body']

                update_welfare.save()

                return redirect('welfare:detail', update_welfare.id)
            
            elif request.method == 'GET':
                edit_welfare = Welfare.objects.get(id = id)
                return render(request, 'welfare/edit.html', {
                    'welfare':edit_welfare,
                    })
        else:
            return render(request, 'accounts/no_auth.html')
    else:
        return render(request, 'accounts/no_auth.html')

def detail(request, welfare_id):
    welfare = get_object_or_404(Welfare, pk = welfare_id)
    comments = WComment.objects.filter(welfare = welfare)
    comments_count = len(comments)
    return render(request, 'welfare/detail.html',{
        'welfare':welfare,
        'comments' : comments,
        'comments_count' : comments_count,
        })


def delete(request, welfare_id):
    if request.user.is_staff:
        delete_welfares = Welfare.objects.get(id = welfare_id)
        if request.user == delete_welfares.writer:
            delete_welfares.delete()
            return redirect('benefits:choose')
        elif request.user.is_superuser:
            delete_welfares.delete()
            return redirect('benefits:choose')
        else:
            return render(request, 'accounts/no_auth.html')

def comment_likes(request, comment_id):
    if request.user.is_authenticated: 
        comment = get_object_or_404(WComment, id=comment_id)
        if request.user in comment.comment_like.all():
            comment.comment_like.remove(request.user)
            comment.comment_like_count -=1
            comment.save()
        else:
            comment.comment_like.add(request.user)
            comment.comment_like_count +=1
            comment.save()
        return redirect('welfare:detail', comment.welfare.id)
    else:
        return render(request, 'accounts/no_auth.html')

def delete_comment(request, comment_id):
    delete_comment = WComment.objects.get(id = comment_id)
    if request.user == delete_comment.writer:
        delete_comment.delete()
        return redirect('welfare:detail', delete_comment.welfare.id)
    elif request.user.is_superuser:
        delete_comment.delete()
        return redirect('welfare:detail', delete_comment.welfare.id)
    else:
        return render(request, 'accounts/no_auth.html')

def edit_comment(request, comment_id):
    if request.user.is_authenticated:
        edit_comment = get_object_or_404(WComment, pk=comment_id)
        if request.user == edit_comment.writer:
            if request.method == 'POST':
                edit_comment.welfare = edit_comment.welfare #게시물 비교하기 위한 공간에 이 게시물 담음
                edit_comment.writer = request.user
                edit_comment.content = request.POST['content'] #댓글 내용 담아담아
                edit_comment.pub_date = timezone.now() #댓글 작성한 시간 담아담아

                edit_comment.save() #댓글 저장, id 생성
            
                return redirect('welfare:detail', edit_comment.welfare.id)
            elif request.method == 'GET':
                welfare = Welfare.objects.get(id = edit_comment.welfare.id)
                comments = WComment.objects.filter(welfare = welfare)
                comments_count = len(comments)
                return render(request, 'welfare/edit_comment.html',{
                    'comment' : edit_comment,
                    'welfare' : welfare,
                    'comments' : comments,
                    'comments_count' : comments_count,
                    })
        elif request.user.is_superuser:
            if request.method == 'POST':
                edit_comment.welfare = edit_comment.welfare #게시물 비교하기 위한 공간에 이 게시물 담음
                edit_comment.writer = request.user
                edit_comment.content = request.POST['content'] #댓글 내용 담아담아
                edit_comment.pub_date = timezone.now() #댓글 작성한 시간 담아담아

                edit_comment.save() #댓글 저장, id 생성
            
                return redirect('welfare:detail', edit_comment.welfare.id)
            if request.method == 'GET':
                welfare = Welfare.objects.get(id = edit_comment.welfare.id)
                comments = WComment.objects.filter(welfare = welfare)
                comments_count = len(comments)
                return render(request, 'welfare/edit_comment.html',{
                    'comment' : edit_comment,
                    'welfare' : welfare,
                    'comments' : comments,
                    'comments_count' : comments_count,
                    })
        else:
            return render(request, 'accounts/no_auth.html')
    else:
        return redirect('accounts:login')


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


def business(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경영대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경영대학") | Welfare.objects.filter(end_date = None, category_univ = "경영대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "경영대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "경영대학") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })

def business_room(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경영대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경영대학", category_type = "공간대여") | Welfare.objects.filter(end_date = None, category_univ = "경영대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "경영대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "경영대학", category_type = "공간대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })

def business_material(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경영대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경영대학", category_type = "물품대여") | Welfare.objects.filter(end_date = None, category_univ = "경영대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "경영대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "경영대학", category_type = "물품대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })

def art(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "예술대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "예술대학") | Welfare.objects.filter(end_date = None, category_univ = "예술대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "예술대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "예술대학") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def art_room(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "예술대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "예술대학", category_type = "공간대여") | Welfare.objects.filter(end_date = None, category_univ = "예술대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "예술대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "예술대학", category_type = "공간대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })

def art_material(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "예술대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "예술대학", category_type = "물품대여") | Welfare.objects.filter(end_date = None, category_univ = "예술대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "예술대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "예술대학", category_type = "물품대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })

def social(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사회과학대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사회과학대학") | Welfare.objects.filter(end_date = None, category_univ = "사회과학대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "사회과학대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "사회과학대학") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def social_room(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사회과학대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사회과학대학", category_type = "공간대여") | Welfare.objects.filter(end_date = None, category_univ = "사회과학대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "사회과학대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "사회과학대학", category_type = "공간대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def social_material(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사회과학대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사회과학대학", category_type = "물품대여") | Welfare.objects.filter(end_date = None, category_univ = "사회과학대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "사회과학대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "사회과학대학", category_type = "물품대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def ai(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "AI융합대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "AI융합대학") | Welfare.objects.filter(end_date = None, category_univ = "AI융합대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "AI융합대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "AI융합대학") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def ai_room(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "AI융합대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "AI융합대학", category_type = "공간대여") | Welfare.objects.filter(end_date = None, category_univ = "AI융합대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "AI융합대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "AI융합대학", category_type = "공간대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def ai_material(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "AI융합대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "AI융합대학", category_type = "물품대여") | Welfare.objects.filter(end_date = None, category_univ = "AI융합대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "AI융합대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "AI융합대학", category_type = "물품대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def engineering(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "공과대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "공과대학") | Welfare.objects.filter(end_date = None, category_univ = "공과대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "공과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "공과대학") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def engineering_room(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "공과대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "공과대학", category_type = "공간대여") | Welfare.objects.filter(end_date = None, category_univ = "공과대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "공과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "공과대학", category_type = "공간대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def engineering_material(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "공과대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "공과대학", category_type = "물품대여") | Welfare.objects.filter(end_date = None, category_univ = "공과대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "공과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "공과대학", category_type = "물품대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def buddhism(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "불교대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "불교대학") | Welfare.objects.filter(end_date = None, category_univ = "불교대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "불교대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "불교대학") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def buddhism_room(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "불교대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "불교대학", category_type = "공간대여") | Welfare.objects.filter(end_date = None, category_univ = "불교대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "불교대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "불교대학", category_type = "공간대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def buddhism_material(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "불교대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "불교대학", category_type = "물품대여") | Welfare.objects.filter(end_date = None, category_univ = "불교대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "불교대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "불교대학", category_type = "물품대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def future(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "미래융합대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "미래융합대학") | Welfare.objects.filter(end_date = None, category_univ = "미래융합대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "미래융합대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "미래융합대학") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def future_room(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "미래융합대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "미래융합대학", category_type = "공간대여") | Welfare.objects.filter(end_date = None, category_univ = "미래융합대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "미래융합대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "미래융합대학", category_type = "공간대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def future_material(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "미래융합대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "미래융합대학", category_type = "물품대여") | Welfare.objects.filter(end_date = None, category_univ = "미래융합대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "미래융합대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "미래융합대학", category_type = "물품대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def science(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "이과대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "이과대학") | Welfare.objects.filter(end_date = None, category_univ = "이과대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "이과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "이과대학") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def science_room(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "이과대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "이과대학", category_type = "공간대여") | Welfare.objects.filter(end_date = None, category_univ = "이과대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "이과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "이과대학", category_type = "공간대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def science_material(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "이과대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "이과대학", category_type = "물품대여") | Welfare.objects.filter(end_date = None, category_univ = "이과대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "이과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "이과대학", category_type = "물품대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def liberal(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "문과대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "문과대학") | Welfare.objects.filter(end_date = None, category_univ = "문과대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "문과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "문과대학") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def liberal_room(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "문과대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "문과대학", category_type = "공간대여") | Welfare.objects.filter(end_date = None, category_univ = "문과대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "문과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "문과대학", category_type = "공간대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def liberal_material(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "문과대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "문과대학", category_type = "물품대여") | Welfare.objects.filter(end_date = None, category_univ = "문과대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "문과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "문과대학", category_type = "물품대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def police(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경찰사법대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경찰사법대학") | Welfare.objects.filter(end_date = None, category_univ = "경찰사법대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "경찰사법대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "경찰사법대학") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def police_room(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경찰사법대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경찰사법대학", category_type = "공간대여") | Welfare.objects.filter(end_date = None, category_univ = "경찰사법대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "경찰사법대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "경찰사법대학", category_type = "공간대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def police_material(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "경찰사법대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "경찰사법대학", category_type = "물품대여") | Welfare.objects.filter(end_date = None, category_univ = "경찰사법대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "경찰사법대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "경찰사법대학", category_type = "물품대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def education(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사범대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사범대학") | Welfare.objects.filter(end_date = None, category_univ = "사범대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "사범대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "사범대학") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def education_room(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사범대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사범대학", category_type = "공간대여") | Welfare.objects.filter(end_date = None, category_univ = "사범대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "사범대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "사범대학", category_type = "공간대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def education_material(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "사범대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "사범대학", category_type = "물품대여") | Welfare.objects.filter(end_date = None, category_univ = "사범대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "사범대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "사범대학", category_type = "물품대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def law(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "법과대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "법과대학") | Welfare.objects.filter(end_date = None, category_univ = "법과대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "법과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "법과대학") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })

def law_room(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "법과대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "법과대학", category_type = "공간대여") | Welfare.objects.filter(end_date = None, category_univ = "법과대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "법과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "법과대학", category_type = "공간대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })


def law_material(request):
    now = timezone.now() #현재 시간 받아옴
    univ = "법과대학"
    welfares_notend = Welfare.objects.filter(start_date__lte = now, end_date__gte = now, category_univ = "법과대학", category_type = "물품대여") | Welfare.objects.filter(end_date = None, category_univ = "법과대학") | Welfare.objects.filter(start_date = None, end_date__gte = now, category_univ = "법과대학").order_by(F('end_date').desc(nulls_last=True)) #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    welfares_end = Welfare.objects.filter(end_date__lt = now, category_univ = "법과대학", category_type = "물품대여") #기간이 지난 게시물들을 받아옴
    
    first_rows_notend = []
    second_rows_notend = []
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
        'univ' : univ,
        'welfares_notend':welfares_notend,
        'first_rows_notend':first_rows_notend,
        'second_rows_notend':second_rows_notend,
        'welfares_end':welfares_end,
        'first_rows_end':first_rows_end,
        'second_rows_end':second_rows_end,
        })

def welfare_like_toggle(request):
    if request.user.is_authenticated: #유저가 로그인했으면
        pk = request.GET["pk"]
        welfare = get_object_or_404(Welfare, pk=pk) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in welfare.welfare_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            welfare.welfare_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            welfare.welfare_like_count -=1 # 좋아요 개수 1개 줄음
            welfare.save() #저장
            result = "like_cancel"
        else:
            welfare.welfare_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            welfare.welfare_like_count +=1 #좋아요 1개 추가
            welfare.save()
            result = "like"

        context = {
            "welfare_like_count" : welfare.welfare_like_count,
            "result" : result
        }

        return HttpResponse(json.dumps(context), content_type = "application/json")
    else:
        return render(request, 'accounts/no_auth.html')
    
def comment_like_toggle(request):
    if request.user.is_authenticated: #유저가 로그인했으면
        pk = request.GET["pk"]
        comment = get_object_or_404(WComment, pk=pk) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
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