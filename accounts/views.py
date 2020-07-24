from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate as django_authenticate
from django.http import JsonResponse

