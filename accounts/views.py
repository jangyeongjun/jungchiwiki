from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import auth
from django.shortcuts import redirect


def signup(request):
    if request.method  == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']
            password = request.POST['password1']
            gender   = request.POST['gender']
            politicalOrientation = request.POST['politicalOrientation']
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            user.profile.gender = gender
            user.profile.politicalOrientation = politicalOrientation
            user.profile.save()
            auth.login(request, user)
            return redirect('/feeds')
    return render(request, 'accounts/signup.html')