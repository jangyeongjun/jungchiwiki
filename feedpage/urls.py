from django.urls import path
from feedpage import views


urlpatterns = [
    path('', views.main, name='main'),
    path('search/', views.search, name='search'),
    path('lawsearch/', views.lawsearch, name='lawsearch'),
    path('politician/<int:pid>/', views.politician, name='politician'), #pid = politician model id
    path('politician/<int:pid>/normalfeed/<int:nfid>/smallfeed/<int:sfid>/like/', views.smallFeed_like, name='smallFeed_like'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/smallfeed/<int:sfid>/dislike/', views.smallFeed_dislike, name='smallFeed_dislike'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/like/', views.normalFeed_like, name='normalFeed_like'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/dislike/', views.normalFeed_dislike, name='normalFeed_dislike'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/', views.normalFeed_debate, name='normalFeed_debate'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/comment/<int:cid>/like/', views.normalFeed_comment_like, name='normalFeed_comment_like'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/comment/<int:cid>/dislike/', views.normalFeed_comment_dislike, name='normalFeed_comment_dislike'),
] 
