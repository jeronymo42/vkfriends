from django.contrib import admin
from django.urls import path
from .views import index, user_registration, user_login, user_logout, friend_request, approve_friend, my_friends, send_requests, get_requests, delete_friend, all_users

urlpatterns = [
    path('', index, name='index'),
    path('registration/', user_registration, name='regis'),
    path('login/', user_login, name='log in'),
    path('logout/', user_logout, name='log out'),
    path('userlist/', all_users, name='all users'),
    path('friend_request/<int:userID>', friend_request, name='friend request'),
    path('approve_friend', approve_friend, name='approve friend'),
    path('myfriends/', my_friends, name='my friends'),
    path('sendrequests/', send_requests, name='send requests'),
    path('getrequests/', get_requests, name='get requests'),
    path('delete_friend/<int:userID>', delete_friend, name='delete'),
]
