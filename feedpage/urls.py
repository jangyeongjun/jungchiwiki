from django.urls import path
from feedpage import views


urlpatterns = [
    path('',                                                                                            views.main,                             name='main'),
    path('search/',                                                                                     views.search,                           name='search'),
    path('search/poliupdate/',                                                                          views.poliupdate,                       name='poliupdate'),
    path('search/<int:page>/',                                                                          views.search,                           name='search'),
    #poliname_v='',poliparty_v='',policommi_v='',polidisstrict_v='',poligender_v='',polielected_v
    path('search/<int:page>/<str:poliname_v>/<str:poliparty_v>/<str:policommi_v>/<str:polidisstrict_v>/<str:poligender_v>/<str:polielected_v>/<str:polihow_v>/<str:poliori_v>/<str:poliAge_v>/',                                                                          views.search,                           name='search'),
    
                                                                                                        
    path('lawsearch/',                                                                                  views.lawsearch,                        name='lawsearch'),
    path('lawsearch/<int:page>/',                                                                       views.lawsearch,                        name='lawsearch'),
    path('lawsearch/<int:page>/<str:lawkey>/',                                                          views.lawsearch,                        name='lawsearch'),
    path('lawsearch/lawupdate/',               
    
                                                                                                        views.lawupdate,                        name='lawupdate'),
    path('politician/<int:pid>/',                                                                       views.politician,                       name='politician'), #pid = politician model id
    path('politician/<int:pid>/insert-photo/',                                                          views.insert_photo,                     name='insert_photo'),
   

    path('politician/<int:pid>/law/<int:lid>/like/',                                                    views.law_like,                         name='law_like'),
    path('politician/<int:pid>/law/<int:lid>/dislike/',                                                 views.law_dislike,                      name='law_dislike'),
    
    path('politician/<int:pid>/law/<int:lid>/debate/',                                                  views.law_debate,                       name='law_debate'),
    
    path('politician/<int:pid>/law/<int:lid>/debate/comment/<int:cid>/like/',                           views.law_debate_comment_like,   name='law_debate_comment_like'),
    path('politician/<int:pid>/law/<int:lid>/debate/comment/<int:cid>/dislike/',                        views.law_debate_comment_dislike,name='law_debate_comment_dislike'),
    path('politician/<int:pid>/law/<int:lid>/debate/comment/new/',                                      views.law_debate_new_comment,    name='law_debate_new_comment'),
    path('politician/<int:pid>/law/<int:lid>/debate/comment/<int:cid>/delete/',                         views.law_debate_comment_delete, name='law_debate_comment_delete'),
    path('politician/<int:pid>/law/<int:lid>/debate/comment/<int:cid>/edit/',                           views.law_debate_comment_edit,   name='law_debate_comment_edit'),

    path('politician/<int:pid>/law/<int:lid>/debate/comment/<int:cid>/ctc/<int:ctcid>/like/',           views.law_debate_ctc_like,       name='law_ctc_like'),
    path('politician/<int:pid>/law/<int:lid>/debate/comment/<int:cid>/ctc/<int:ctcid>/dislike/',        views.law_debate_ctc_dislike,    name='law_ctc_dislike'),
    path('politician/<int:pid>/law/<int:lid>/debate/comment/<int:cid>/ctc/<int:ctcid>/delete/',         views.law_debate_ctc_delete,     name='law_ctc_delete'),
    path('politician/<int:pid>/law/<int:lid>/debate/comment/<int:cid>/new/',                            views.law_debate_new_CTC,        name='lawnormalFeed_debate_new_comment'),
    path('politician/<int:pid>/law/<int:lid>/debate/comment/<int:cid>/ctc/<int:ctcid>/edit/',           views.law_debate_ctc_edit,       name='law_ctc_edit'),



    path('politician/<int:pid>/orientationVote/<int:value>/',                                           views.orientationVote,                  name='orientationVote'),
    path('politician/<int:pid>/orientationVote/cancel/',                                                views.orientationVoteCancel,            name='orientationVoteCancel'),
    
    path('politician/<int:pid>/normalfeed/<int:nfid>/like/',                                            views.normalFeed_like,                  name='normalFeed_like'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/dislike/',                                         views.normalFeed_dislike,               name='normalFeed_dislike'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/edit/',                                            views.normalFeed_edit,                  name='normalFeed_edit'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/delete/',                                          views.normalFeed_delete,                name='normalFeed_delete'),
    #information용
    path('politician/<int:pid>/normalfeed/<int:nfid>/infor/',                                           views.pie_chart,                        name='pie_chart'),
    path('politician/<int:pid>/normalfeed/new/',                                                        views.normalFeedAdd,                    name='normalFeedAdd'),
    path('politician/<int:pid>/normalfeed/create/',                                                     views.normalFeedCreate,                 name='normalFeedCreate'),

    path('politician/<int:pid>/normalfeed/<int:nfid>/smallfeed/<int:sfid>/like/',                       views.smallFeed_like,                   name='smallFeed_like'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/smallfeed/<int:sfid>/dislike/',                    views.smallFeed_dislike,                name='smallFeed_dislike'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/smallfeed/<int:sfid>/edit/',                       views.smallFeed_edit,                   name='smallFeed_edit'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/smallfeed/<int:sfid>/delete/',                     views.smallFeed_delete,                 name='smallFeed_delete'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/smallfeed/new/',                                   views.smallFeedAdd,                     name='smallFeedAdd'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/smallfeed/create/',                                views.smallFeedCreate,                  name='smallFeedCreate'),
   
   
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/',                                          views.normalFeed_debate,                name='normalFeed_debate'),
    
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/like/',                   views.normalFeed_debate_comment_like,   name='normalFeed_debate_comment_like'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/dislike/',                views.normalFeed_debate_comment_dislike,name='normalFeed_debate_comment_dislike'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/new/',                              views.normalFeed_debate_new_comment,    name='normalFeed_debate_new_comment'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/delete/',                 views.normalFeed_debate_comment_delete, name='normalFeed_debate_comment_delete'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/edit/',                   views.normalFeed_debate_comment_edit,   name='normalFeed_debate_comment_edit'),

    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/ctc/<int:ctcid>/like/',   views.normalFeed_debate_ctc_like,       name='normalFeed_ctc_like'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/ctc/<int:ctcid>/dislike/',views.normalFeed_debate_ctc_dislike,    name='normalFeed_ctc_dislike'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/ctc/<int:ctcid>/delete/', views.normalFeed_debate_ctc_delete,     name='normalFeed_ctc_delete'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/new/',                    views.normalFeed_debate_new_CTC,        name='normalFeed_debate_new_comment'),
    path('politician/<int:pid>/normalfeed/<int:nfid>/debate/comment/<int:cid>/ctc/<int:ctcid>/edit/',   views.normalFeed_debate_ctc_edit,       name='normalFeed_ctc_edit'),

] 

