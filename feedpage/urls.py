from django.urls import path
from feedpage import views


urlpatterns = [
    path('', views.main, name='main'),
    path('search/', views.search, name='search'),
    #path('', views.politician, name='politician'),
] 
