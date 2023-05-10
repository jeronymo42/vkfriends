from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, FriendRequest
from rest_framework.pagination import PageNumberPagination

menu = {'Пользователи': 'all users', 'Мои друзья': 'my friends', 'Исходящие запросы': 'send requests', 'Мои запросы': 'get requests', 'Выйти':'log out'}
status = {'Не друзья', 'Отправлена заявка', 'Получена заявка', 'Друзья'}

def index(request):
    return render(request, 'index.html', context={})

def user_registration(request):
    context = {}
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('log in')
        else:
            print("Form is not valid")
    context['form'] = RegistrationForm()
    context['menu'] = menu
    return render(request, 'users/registration.html', context=context)


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('all users')
        else:
            return redirect('log in')
    else:
        form = LoginForm()
        context = {}
        context['form'] = form
        context['menu'] = menu
    return render(request, 'users/login.html', context=context)

@login_required
def user_logout(request):
    logout(request)
    return redirect('log in')

@login_required
def friend_request(request, userID):
    from_user = request.user
    to_user = User.objects.get(id=userID)
    counter_request = FriendRequest.objects.filter(from_user=to_user, to_user=from_user)
    relation = FriendRequest.objects.filter(from_user=from_user, to_user=to_user)
    if counter_request.exists() or relation.exists():
        FriendRequest.objects.filter(from_user=to_user, to_user=from_user).update(status = 2)
        return redirect('my friends')
    created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user, status=1)
    if created:
        return redirect('send requests')
    return HttpResponse('Запрос на дружбу был направлен ранее...')

@login_required
def send_requests(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    context = {}
    context['menu'] = menu
    context['title'] = 'Отправленные запросы'
    context['status'] = 'Отправлен запрос...'
    context['requests'] = []
    to_user = FriendRequest.objects.values('to_user').filter(from_user=request.user, status=1)
    for i in to_user:
        context['requests'].append(User.objects.get(id=i['to_user']))
    return render(request, 'users/requestlist.html', context=context)

@login_required
def get_requests(request):
    context = {}
    context['menu'] = menu
    context['title'] = 'Запросы на дружбу'
    context['status'] = 'Получен запрос'
    context['requests'] = []
    to_user = FriendRequest.objects.values('from_user').filter(to_user=request.user, status=1)
    for i in to_user:
        context['requests'].append(User.objects.get(id=i['from_user']))
    return render(request, 'users/requestlist.html', context=context)

@login_required
def my_friends(request):
    context = {}
    context['menu'] = menu
    friend_ids = []
    to_user = FriendRequest.objects.values('to_user').filter(from_user=request.user, status=2)
    from_user = FriendRequest.objects.values('from_user').filter(to_user=request.user, status=2)
    for i in to_user:
        friend_ids.append(i['to_user'])
    for i in from_user:
        friend_ids.append(i['from_user'])
    context['friends'] = []
    for i in friend_ids:
        context['friends'].append(User.objects.get(id=i))
    return render(request, 'users/friendslist.html', context=context)

@login_required
def approve_friend(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return redirect('my friends')
    return HttpResponse('Заявка отклонена')

@login_required
def delete_friend(request, userID):
    userid = User.objects.values('id').filter(username=request.user)[:1]
    if FriendRequest.objects.filter(from_user=userID, to_user=userid).exists():
        FriendRequest.objects.filter(from_user=userID, to_user=userid).delete()
    else:
        FriendRequest.objects.filter(to_user=userID, from_user=userid).delete()
    return redirect('my friends')
    
@login_required
def all_users(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    context = {}
    context['menu'] = menu
    context['title'] = 'Все пользователи'
    context['users'] = []
    context['status'] = {}
    for i in User.objects.all().exclude(username = request.user):
        context['users'].append(i)
        if FriendRequest.objects.filter(from_user=request.user, to_user=i.id).exclude(status=2):
            context['status'][i.id] = 'Направлен запрос'
            continue
        if FriendRequest.objects.filter(to_user=request.user, from_user=i.id).exclude(status=2):
            context['status'][i.id] = 'Получен запрос'
            continue
        if FriendRequest.objects.filter(to_user=request.user, from_user=i.id, status=2) or FriendRequest.objects.filter(from_user=request.user, to_user=i.id, status=2):
            context['status'][i.id] = 'Друзья'
            continue
        context['status'][i.id] = 'Пока не друзья'
    return render(request, 'users/userlist.html', context=context)