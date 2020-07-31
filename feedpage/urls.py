from django.urls import path
from feedpage import views


urlpatterns = [
    path('', views.main, name='main'),
    path('search/', views.search, name='search'),
    path('', views.search, name='search'),
    path('politician/<int:pid>/', views.politician, name='politician'), #pid = politician model id
    path('politician/<int:pid>/orientationVote/<int:value>/', views.orientationVote, name='orientationVote'),
    path('politician/<int:pid>/orientationVote/cancel/', views.orientationVoteCancel, name='orientationVoteCancel'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/smallfeed/<int:sfid>/like/', views.smallFeed_like, name='smallFeed_like'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/smallfeed/<int:sfid>/dislike/', views.smallFeed_dislike, name='smallFeed_dislike'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/like/', views.normalFeed_like, name='normalFeed_like'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/dislike/', views.normalFeed_dislike, name='normalFeed_dislike'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/', views.normalFeed_debate, name='normalFeed_debate'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/like/', views.normalFeed_comment_like, name='normalFeed_comment_like'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/dislike/', views.normalFeed_comment_dislike, name='normalFeed_comment_dislike'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/new/', views.normalFeed_debate_new_comment, name='normalFeed_debate_new_comment'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/new/', views.normalFeed_debate_new_CTC, name='normalFeed_debate_new_comment'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/ctc/<int:ctcid>/like/', views.normalFeed_ctc_like, name='normalFeed_ctc_like'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/ctc/<int:ctcid>/dislike/', views.normalFeed_ctc_dislike, name='normalFeed_ctc_dislike'),
] 
