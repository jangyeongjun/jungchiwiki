from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Politician 

# Create your views here.
def main(request):
    return render(request,'feedpage/main.html')
 
def search(request):
    return render(request,'feedpage/search.html')


def politician(request, pid):
    politician = Politician.objects.get(id = pid)
    return render(request,'feedpage/politician.html', {'politician': politician})