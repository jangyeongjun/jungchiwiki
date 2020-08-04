from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate as django_authenticate
from django.http import JsonResponse


def signup(request):
    print("가입하기 눌림")
    print(request.POST)
    if request.method == "POST":
       username = request.POST["username"]
       nickname = request.POST['usernickname']
       gender = request.POST["usergender"]
       birth_dt = request.POST["userbirth_dt"]
       politicalOrientation = request.POST["user_Orientation"]
       password = request.POST["password1"]

       user = User.objects.create_user(username=username, password=password)
       user.profile.gender = gender
       user.profile.nickname=nickname
       user.profile.birth_dt=birth_dt
       user.profile.politicalOrientation=politicalOrientation
       user.save()

       login_user = django_authenticate(username=username, password=password)
       django_login(request, login_user)
       return JsonResponse({"response": "signup success"})