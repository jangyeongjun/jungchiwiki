from django.urls import path
from feedpage import views


urlpatterns = [
    path('', views.main, name='main'),
    path('', views.search, name='search'),
    path('politician/<int:pid>', views.politician, name='politician'), #pid = politician model id
] 
