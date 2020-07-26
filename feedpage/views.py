from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User


# Create your views here.
def main(request):
    return render(request,'feedpage/main.html')
 
def search(request):
    return render(request,'feedpage/search.html')


def politician(request):
    return render(request,'feedpage/politician.html')