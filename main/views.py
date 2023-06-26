from django.shortcuts import render, redirect, get_object_or_404
from .models import MainPost, MainComment
from django.utils import timezone


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

    for index, culture_post in enumerate(culture_posts):
        if (index+1)%6 == 1:
            culture_posts_1.append(culture_post)
        elif (index+1)%6 == 2:
            culture_posts_2.append(culture_post)
        elif (index+1)%6 == 3:
            culture_posts_3.append(culture_post)
        elif (index+1)%6 == 4:
            culture_posts_4.append(culture_post)
        elif (index+1)%6 == 5:
            culture_posts_5.append(culture_post)
        elif (index+1)%6 == 6:
            culture_posts_6.append(culture_post)

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
            return redirect('main:choose')
        elif request.user.is_superuser:
            delete_mainpost.delete()
            return redirect('main:choose')
        else:
            return render(request, 'accounts/no_auth.html')
    else:
        return render(request, 'accounts/no_auth.html')

def comment_likes(request, comment_id):
    if request.user.is_authenticated: 
        comment = get_object_or_404(MainComment, id=comment_id)
        if request.user in comment.comment_like.all():
            comment.comment_like.remove(request.user)
            comment.comment_like_count -=1
            comment.save()
        else:
            comment.comment_like.add(request.user)
            comment.comment_like_count +=1
            comment.save()
        return redirect('main:detail', comment.mainpost.id)
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
