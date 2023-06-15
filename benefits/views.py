from django.shortcuts import render, redirect, get_object_or_404
from .models import Benefit
from accounts.models import CustomUser
from django.utils import timezone


def mainpage(request):
    empty_post = Benefit.objects.filter(title='')
    empty_post.delete()
    now = timezone.now() #현재 시간 받아옴
    posts = Benefit.objects.filter(start_date__lt = now, due_date__gt = now).order_by('due_date') #현재 시간이 기간 내에 있는 게시물들을 받아오고 끝나는 기간이 이른 순서대로 나열함
    end_posts = Benefit.objects.filter(due_date__lt = now) #기간이 지난 게시물들을 받아옴
    post_first_line = [] #기간 내에 있는 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    post_second_line = [] #기간 내에 있는 게시물들 중 둘째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_first_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련
    end_second_line = [] #기간 지난 게시물들 중 첫째 줄에 들어갈 게시물들이 들어갈 공간 마련

    for i, post in enumerate(posts): #enumerate 함수는 찾아본 결과 순서가 있는 자료형을 인덱스와 해당 요소를 포함하는 객체를 반환한다 해서 사용함 (순서번호 객체)
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            post_first_line.append(post) #담아담아
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            post_second_line.append(post) #담아담아

    if len(post_second_line) < len(post_first_line): #두번 째 쭐에 있는 게시물들이 첫번 째 줄에 있는 게시물보다 적으면 빈 객체를 넣어서 수를 맞춰줌. 이거 안하면 제휴 끝난 게시물 위치가 이상해짐
        empty_object = Benefit() #빈 객체를 생성함
        empty_object.title = ''
        empty_object.writer = CustomUser.objects.get(username='sam') #ForeignKey로 writer과 User을 연결했다보니 이건 무조건 필요하다하여 그냥 관리자 계정 넣어놓은거임
        empty_object.start_date = None
        empty_object.due_date = None
        empty_object.image = None
        empty_object.body = ''
        
        empty_object.save()

        post_second_line.append(empty_object) #빈 객체도 이제 두번 째 줄 게시물에 추가시킴
    
    for i, end_post in enumerate(end_posts):
        if (i+1) % 2 == 1: #짝수 번째에 있는 게시물들
            end_first_line.append(end_post)
        elif (i+1) % 2 == 0: #홀수 번째에 있는 게시물들
            end_second_line.append(end_post) #담아담아

    return render(request, 'benefits/mainpage.html', {
        'post_first_line':post_first_line,
        'post_second_line':post_second_line,
        'end_first_line':end_first_line,
        'end_second_line':end_second_line,
        })


def create(request):
    new_benefit = Benefit()
    new_benefit.title = request.POST['title']
    new_benefit.writer = request.user
    new_benefit.start_date = request.POST['start_date']
    new_benefit.due_date = request.POST['due_date']
    new_benefit.image = request.FILES.get('image')
    new_benefit.body = request.POST['body']

    new_benefit.save()
    
    return redirect('benefits:detail', new_benefit.id)

def new(request):
    return render(request, 'benefits/new.html')

def detail(request, id):
    benefit = get_object_or_404(Benefit, pk = id)
    return render(request, 'benefits/detail.html',{
        'benefit':benefit,
        })

def edit(request, id):
    edit_benefit = Benefit.objects.get(id = id)
    return render(request, 'benefits/edit.html', {
        'benefit':edit_benefit,
    })

def update(request, id):
    update_benefit = Benefit.objects.get(id = id)
    update_benefit.title = request.POST['title']
    update_benefit.writer = request.user
    update_benefit.start_date = request.POST['start_date']
    update_benefit.due_date = request.POST['due_date']
    update_benefit.image = request.FILES.get('image', update_benefit.image)
    update_benefit.body = request.POST['body']

    update_benefit.save()

    return redirect('benefits:detail', update_benefit.id)

def delete(request, id):
    delete_benefits = Benefit.objects.get(id = id)
    delete_benefits.delete()
    return redirect('benefits:mainpage')

def mainpage_likes(request, benefit_id):
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
        return redirect('benefits:mainpage')
    else:
        return render(request, 'accounts/no_auth.html')


def detail_likes(request, benefit_id):
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
        return redirect('benefits:detail', benefit.id)
    else:
        return render(request, 'accounts/no_auth.html')

