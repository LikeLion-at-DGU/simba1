from django.shortcuts import render, redirect, get_object_or_404
from .models import MainPost, MainComment
from django.utils import timezone
from django.http import HttpResponse
import json


def intro(request):
    return render(request, 'main/intro.html')

def mainpage(request):
    culture_posts = MainPost.objects.filter(category_type = "문화생활")
    cafe_posts = MainPost.objects.filter(category_type = "카페&식당") #기간이 지난 게시물들을 받아옴
    etc_posts = MainPost.objects.filter(category_type = "기타 서비스")

    culture_posts_1 = []
    culture_posts_2 = []
    culture_posts_3 = []
    culture_posts_4 = []
    culture_posts_5 = []
    culture_posts_6 = []
    culture_posts_7 = []
    culture_posts_8 = []
    culture_posts_9 = []
    culture_posts_10 = []

    cafe_posts_1 = []
    cafe_posts_2 = []
    cafe_posts_3 = []
    cafe_posts_4 = []
    cafe_posts_5 = []
    cafe_posts_6 = []
    cafe_posts_7 = []
    cafe_posts_8 = []
    cafe_posts_9 = []
    cafe_posts_10 = []

    etc_posts_1 = []
    etc_posts_2 = []
    etc_posts_3 = []
    etc_posts_4 = []
    etc_posts_5 = []
    etc_posts_6 = []
    etc_posts_7 = []
    etc_posts_8 = []
    etc_posts_9 = []
    etc_posts_10 = []

    for index, culture_post in enumerate(culture_posts):
        if (index+1)%11 == 1:
            culture_posts_1.append(culture_post)
        elif (index+1)%11 == 2:
            culture_posts_2.append(culture_post)
        elif (index+1)%11 == 3:
            culture_posts_3.append(culture_post)
        elif (index+1)%11 == 4:
            culture_posts_4.append(culture_post)
        elif (index+1)%11 == 5:
            culture_posts_5.append(culture_post)
        elif (index+1)%11 == 6:
            culture_posts_6.append(culture_post)
        elif (index+1)%11 == 7:
            culture_posts_7.append(culture_post)
        elif (index+1)%11 == 8:
            culture_posts_8.append(culture_post)
        elif (index+1)%11 == 9:
            culture_posts_9.append(culture_post)
        elif (index+1)%11 == 10:
            culture_posts_10.append(culture_post)

    for index, cafe_post in enumerate(cafe_posts):
        if (index+1)%11 == 1:
            cafe_posts_1.append(cafe_post)
        elif (index+1)%11 == 2:
            cafe_posts_2.append(cafe_post)
        elif (index+1)%11 == 3:
            cafe_posts_3.append(cafe_post)
        elif (index+1)%11 == 4:
            cafe_posts_4.append(cafe_post)
        elif (index+1)%11 == 5:
            cafe_posts_5.append(cafe_post)
        elif (index+1)%11 == 6:
            cafe_posts_6.append(cafe_post)
        elif (index+1)%11 == 7:
            cafe_posts_7.append(cafe_post)
        elif (index+1)%11 == 8:
            cafe_posts_8.append(cafe_post)
        elif (index+1)%11 == 9:
            cafe_posts_9.append(cafe_post)
        elif (index+1)%11 == 10:
            cafe_posts_10.append(cafe_post)

    for index, etc_post in enumerate(etc_posts):
        if (index+1)%11 == 1:
            etc_posts_1.append(etc_post)
        elif (index+1)%11 == 2:
            etc_posts_2.append(etc_post)
        elif (index+1)%11 == 3:
            etc_posts_3.append(etc_post)
        elif (index+1)%11 == 4:
            etc_posts_4.append(etc_post)
        elif (index+1)%11 == 5:
            etc_posts_5.append(etc_post)
        elif (index+1)%11 == 6:
            etc_posts_6.append(etc_post)
        elif (index+1)%11 == 7:
            etc_posts_7.append(etc_post)
        elif (index+1)%11 == 8:
            etc_posts_8.append(etc_post)
        elif (index+1)%11 == 9:
            etc_posts_9.append(etc_post)
        elif (index+1)%11 == 10:
            etc_posts_10.append(etc_post)

    # for index, first_culture_post in enumerate(cultureposts)

    return render(request, 'main/mainpage.html', {
        'culture_posts' : culture_posts,
        'cafe_posts' : cafe_posts,
        "etc_posts" : etc_posts,
        'culture_posts_1' : culture_posts_1,
        'culture_posts_2' : culture_posts_2,
        'culture_posts_3' : culture_posts_3,
        'culture_posts_4' : culture_posts_4,
        'culture_posts_5' : culture_posts_5,
        'culture_posts_6' : culture_posts_6,
        'culture_posts_7' : culture_posts_7,
        'culture_posts_8' : culture_posts_8,
        'culture_posts_9' : culture_posts_9,
        'culture_posts_10' : culture_posts_10,
        'cafe_posts_1' : cafe_posts_1,
        'cafe_posts_2' : cafe_posts_2,
        'cafe_posts_3' : cafe_posts_3,
        'cafe_posts_4' : cafe_posts_4,
        'cafe_posts_5' : cafe_posts_5,
        'cafe_posts_6' : cafe_posts_6,
        'cafe_posts_7' : cafe_posts_7,
        'cafe_posts_8' : cafe_posts_8,
        'cafe_posts_9' : cafe_posts_9,
        'cafe_posts_10' : cafe_posts_10,
        'etc_posts_1' : etc_posts_1,
        'etc_posts_2' : etc_posts_2,
        'etc_posts_3' : etc_posts_3,
        'etc_posts_4' : etc_posts_4,
        'etc_posts_5' : etc_posts_5,
        'etc_posts_6' : etc_posts_6,
        'etc_posts_7' : etc_posts_7,
        'etc_posts_8' : etc_posts_8,
        'etc_posts_9' : etc_posts_9,
        'etc_posts_10' : etc_posts_10,
    })

def create(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                new_mainpost = MainPost()

                new_mainpost.title = request.POST['title']
                new_mainpost.writer = request.user
                new_mainpost.pub_date = timezone.now()
                new_mainpost.category_type = request.POST['category_type']
                if request.POST['start_time']:
                    new_mainpost.start_time = request.POST['start_time']
                if request.POST['end_time']:
                    new_mainpost.end_time = request.POST['end_time']
                new_mainpost.address = request.POST['address']
                new_mainpost.image = request.FILES.get('image')
                new_mainpost.body = request.POST['body']

                new_mainpost.save()
                
                return redirect('main:detail', new_mainpost.id)
            
            elif request.method == 'GET':
                return render(request, 'main/new.html')
            
        else:
            return render(request, 'accounts/no_auth.html')
    else:
        return redirect('accounts:login')

def detail(request, mainpost_id):
    mainpost = get_object_or_404(MainPost, pk = mainpost_id)
    comments = MainComment.objects.filter(mainpost = mainpost)
    comments_count = len(comments)
    return render(request, 'main/detail.html',{
        'mainpost' : mainpost,
        'comments' : comments,
        'comments_count' : comments_count,
        })

def review(request, mainpost_id):#댓글 작성하는 칸
    if request.user.is_authenticated:
        mainpost = MainPost.objects.get(id = mainpost_id) #게시물 id에 맞는 게시물을 담음
        if request.method == 'POST':
            new_comment = MainComment() #댓글 빈 객체 생성
            new_comment.mainpost = mainpost #게시물 비교하기 위한 공간에 이 게시물 담음
            new_comment.writer = request.user
            new_comment.content = request.POST['content'] #댓글 내용 담아담아
            new_comment.mainpost_rate = request.POST['mainpost_rate'] #평점 담아담아
            new_comment.pub_date = timezone.now() #댓글 작성한 시간 담아담아

            new_comment.save() #댓글 저장, id 생성
        
            return redirect('main:detail', mainpost.id)
    
        elif request.method == 'GET':
            mainpost = MainPost.objects.get(id = mainpost_id)
            comments = MainComment.objects.filter(mainpost = mainpost)
            comments_count = len(comments)
            return render(request, 'main/review.html',{
                'mainpost' : mainpost,
                'comments' : comments,
                'comments_count' : comments_count,
                })
    else:
        return redirect('accounts:login')

def update(request, mainpost_id):
    if request.user.is_staff:
        update_mainpost = MainPost.objects.get(id = mainpost_id)
        if request.user == update_mainpost.writer:
            if request.method == 'POST':
                update_mainpost.title = request.POST['title']
                update_mainpost.writer = request.user
                if request.POST['start_time']:
                    update_mainpost.start_time = request.POST['start_time']
                if request.POST['end_time']:
                    update_mainpost.end_time = request.POST['end_time']
                update_mainpost.address = request.POST['address']
                update_mainpost.image = request.FILES.get('image', update_mainpost.image)
                update_mainpost.body = request.POST['body']

                update_mainpost.save()

                return redirect('main:detail', update_mainpost.id)
            
            elif request.method == 'GET':
                edit_mainpost = MainPost.objects.get(id = mainpost_id)
                return render(request, 'main/edit.html', {
                    'mainpost' : edit_mainpost,
                    })
        elif request.user.is_superuser:
            if request.method == 'POST':
                update_mainpost.title = request.POST['title']
                update_mainpost.writer = request.user
                if request.POST['start_time']:
                    update_mainpost.start_time = request.POST['start_time']
                if request.POST['end_time']:
                    update_mainpost.end_time = request.POST['end_time']
                update_mainpost.address = request.POST['address']
                update_mainpost.image = request.FILES.get('image', update_mainpost.image)
                update_mainpost.body = request.POST['body']

                update_mainpost.save()

                return redirect('main:detail', update_mainpost.id)
            
            elif request.method == 'GET':
                edit_mainpost = MainPost.objects.get(id = id)
                return render(request, 'main/edit.html', {
                    'mainpost':edit_mainpost,
                    })
        else:
            return render(request, 'accounts/no_auth.html')
    else:
        return render(request, 'accounts/no_auth.html')

def delete(request, mainpost_id):
    if request.user.is_staff:
        delete_mainpost = MainPost.objects.get(id = mainpost_id)
        if request.user == delete_mainpost.writer:
            delete_mainpost.delete()
            return redirect('main:mainpage')
        elif request.user.is_superuser:
            delete_mainpost.delete()
            return redirect('main:mainpage')
        else:
            return render(request, 'accounts/no_auth.html')
    else:
        return render(request, 'accounts/no_auth.html')

def mainpost_like_toggle(request):
    if request.user.is_authenticated: #유저가 로그인했으면
        pk = request.GET["pk"]
        mainpost = get_object_or_404(MainPost, pk=pk) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
        if request.user in mainpost.mainpost_like.all(): #게시물의 like 안에 있는 모든 유저들 중에 현재 유저가 있는지 판별
            mainpost.mainpost_like.remove(request.user) #이미 좋아요가 눌러진 상태라는 것이기에 좋아요를 누르면 like안에 있는 유저들 중 자기를 없앰
            mainpost.mainpost_like_count -=1 # 좋아요 개수 1개 줄음
            mainpost.save() #저장
            result = "like_cancel"
        else:
            mainpost.mainpost_like.add(request.user) #좋아요를 누르면 like 안에 유저 추가
            mainpost.mainpost_like_count +=1 #좋아요 1개 추가
            mainpost.save()
            result = "like"

        context = {
            "mainpost_like_count" : mainpost.mainpost_like_count,
            "result" : result
        }

        return HttpResponse(json.dumps(context), content_type = "application/json")
    else:
        return render(request, 'accounts/no_auth.html')
    
def comment_like_toggle(request):
    if request.user.is_authenticated: #유저가 로그인했으면
        pk = request.GET["pk"]
        comment = get_object_or_404(MainComment, pk=pk) #URL 매핑으로 받은 게시물 아이디에 해당하는 게시물을 담음
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


def delete_comment(request, comment_id):
    delete_comment = MainComment.objects.get(id = comment_id)
    if request.user == delete_comment.writer:
        delete_comment.delete()
        return redirect('main:detail', delete_comment.mainpost.id)
    elif request.user.is_superuser:
        delete_comment.delete()
        return redirect('main:detail', delete_comment.mainpost.id)
    else:
        return render(request, 'accounts/no_auth.html')

def edit_comment(request, comment_id):
    if request.user.is_authenticated:
        edit_comment = get_object_or_404(MainComment, pk=comment_id)
        if request.user == edit_comment.writer:
            if request.method == 'POST':
                edit_comment.mainpost = edit_comment.mainpost #게시물 비교하기 위한 공간에 이 게시물 담음
                edit_comment.writer = request.user
                edit_comment.content = request.POST['content'] #댓글 내용 담아담아
                edit_comment.mainpost_rate = request.POST['mainpost_rate'] #평점 담아담아
                edit_comment.pub_date = timezone.now() #댓글 작성한 시간 담아담아

                edit_comment.save() #댓글 저장, id 생성
            
                return redirect('main:detail', edit_comment.mainpost.id)
            elif request.method == 'GET':
                mainpost = MainPost.objects.get(id = edit_comment.mainpost.id)
                comments = MainComment.objects.filter(mainpost = mainpost)
                comments_count = len(comments)
                return render(request, 'main/edit_comment.html',{
                    'comment' : edit_comment,
                    'mainpost' : mainpost,
                    'comments' : comments,
                    'comments_count' : comments_count,
                    })
        elif request.user.is_superuser:
            if request.method == 'POST':
                edit_comment.mainpost = edit_comment.mainpost #게시물 비교하기 위한 공간에 이 게시물 담음
                edit_comment.writer = request.user
                edit_comment.content = request.POST['content'] #댓글 내용 담아담아
                edit_comment.mainpost_rate = request.POST['mainpost_rate'] #평점 담아담아
                edit_comment.pub_date = timezone.now() #댓글 작성한 시간 담아담아

                edit_comment.save() #댓글 저장, id 생성
            
                return redirect('main:detail', edit_comment.mainpost.id)
            elif request.method == 'GET':
                mainpost = MainPost.objects.get(id = edit_comment.mainpost.id)
                comments = MainComment.objects.filter(mainpost = mainpost)
                comments_count = len(comments)
                return render(request, 'main/edit_comment.html',{
                    'comment' : edit_comment,
                    'mainpost' : mainpost,
                    'comments' : comments,
                    'comments_count' : comments_count,
                    })
        else:
            return render(request, 'accounts/no_auth.html')
    else:
        return redirect('accounts:login')
    
def detail_likes(request, mainpost_id): # 게시물 안에서 좋아요 누를 때
    if request.user.is_authenticated: #위와 동일
        mainpost = get_object_or_404(MainPost, id=mainpost_id)
        if request.user in mainpost.mainpost_like.all():
            mainpost.mainpost_like.remove(request.user)
            mainpost.mainpost_like_count -=1
            mainpost.save()
        else:
            mainpost.mainpost_like.add(request.user)
            mainpost.mainpost_like_count +=1
            mainpost.save()
        return redirect('main:detail', mainpost.id)
    else:
        return render(request, 'accounts/no_auth.html')
