from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import auth
from django.shortcuts import redirect
# from django.contrib.auth import login as django_login
# from django.contrib.auth import authenticate as django_authenticate
# from django.http import JsonResponse

#모달 시 발
# def signup(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password1"]
#         gender = request.POST["college"]
#         politicalOrientation = request.POST["major"]

#         user = User.objects.create_user(username=username, password=password)
#         user.profile.gender = gender
#         user.profile.politicalOrientation = politicalOrientation
#         user.save()
#         login_user = django_authenticate(username=username, password=password)
#         django_login(request, login_user)
#         return JsonResponse({"response": "signup success"})




def signup(request):
    if request.method  == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']
            password = request.POST['password1']
            gender   = request.POST['gender']
            politicalOrientation = request.POST['politicalOrientation']
            user = User.objects.create_user(username=username, password=password)
            user.profile.nickname = username
            user.profile.gender = gender
            user.profile.politicalOrientation = int(politicalOrientation)
            user.profile.save()
            auth.login(request, user)
            return redirect('/feeds/')
        else:
            # 비밀번호가 일치하지 않는다고 경고 메시지 띄우기
            return render(request, 'accounts/signup.html')
    return render(request, 'accounts/signup.html')