from django.shortcuts import render, get_list_or_404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import *
from .crawling import lawParsing
from .crawling import poliParsing
import os
from django.http import JsonResponse
import simplejson as json
import math


# Create your views here.
def main(request):
    politicians = Politician.objects.all()
    return render(request,'feedpage/main.html', {'politicians' : politicians})
 


def poliupdate(request):
    polis = poliParsing()
    for number in range(len(polis)):
        print(number)
        Politician.objects.create(hg_name = polis[number]['HG_NM'], eng_name = polis[number]['ENG_NM'], bth_name=polis[number]['BTH_GBN_NM'], bth_date=polis[number]['BTH_DATE'], job_res_name = polis[number]['JOB_RES_NM'], politicalParty = polis[number]['POLY_NM'], district = polis[number]['ORIG_NM'], politicalCommittee = polis[number]['CMITS'], electedCount = polis[number]['REELE_GBN_NM'], units = polis[number]['UNITS'], gender = polis[number]['SEX_GBN_NM'], tel_num = polis[number]['TEL_NO'], e_mail = polis[number]['E_MAIL'], homepage = polis[number]['HOMEPAGE'])
    return render(request,'feedpage/search.html')


#===============================================
#CREATE
def insert_photo(request, pid):
    politician = Politician.objects.get(id = pid)
    photo =  request.FILES.get('photo', False) 
    politician.photo = photo
    politician.save()
    path = os.path.join('/feeds/politician/', str(pid))
    return redirect(path)

def normalFeedAdd(request, pid):
    politician = Politician.objects.get(id = pid)
    return render (request,'feedpage/newNormalFeed.html', {'politician': politician})

def normalFeedCreate(request, pid):
    politician = Politician.objects.get(id = pid)
    title = request.POST['title']
    content = request.POST['content']
    if title == '개요':
        title = '1'
    elif title == '경력':
        title = '2'
    elif title == '과거 공약/이행률':
        title = '3'
    elif title == '발의 법률안':
        title = '4'
    elif title =='찬성/반대 법안':
        title = '5'
    else:
        title = '6'
    NormalFeed.objects.create(title = title, content = content, author=request.user, politician=politician)
    path = os.path.join('/feeds/politician/', str(pid))
    return redirect(path)

def smallFeedAdd(request, pid, nfid):
    politician = Politician.objects.get(id = pid)
    normalFeed = NormalFeed.objects.get(id = nfid)
    return render (request,'feedpage/newSmallFeed.html', {'politician': politician, 'normalFeed' : normalFeed})

def smallFeedCreate(request,pid,nfid):
    normalFeed = NormalFeed.objects.get(id = nfid)
    title = request.POST['title']
    content = request.POST['content']
    SmallFeed.objects.create(title = title, content = content, author=request.user, normalFeed=normalFeed)
    path = os.path.join('/feeds/politician/', str(pid))
    return redirect(path)



#===========================================================
#READ  
def polisearch(request):
    polis = poliParsing()
    for number in range(len(polis)):
        print(number)
        Politician.objects.create(hg_name = polis[number]['HG_NM'], eng_name = polis[number]['ENG_NM'], bth_name=polis[number]['BTH_GBN_NM'], bth_date=polis[number]['BTH_DATE'], job_res_name = polis[number]['JOB_RES_NM'], politicalParty = polis[number]['POLY_NM'], district = polis[number]['ORIG_NM'], politicalCommittee = polis[number]['CMITS'], electedCount = polis[number]['REELE_GBN_NM'], units = polis[number]['UNITS'], gender = polis[number]['SEX_GBN_NM'], tel_num = polis[number]['TEL_NO'], e_mail = polis[number]['E_MAIL'], homepage = polis[number]['HOMEPAGE'])
    return render(request,'feedpage/search.html')

def lawsearch(request):
    return render(request, 'feedpage/lawsearch.html')

def main(request):
    politicians = Politician.objects.all()
    return render(request,'feedpage/main.html', {'politicians' : politicians})
 
def search(request, page=1):
    polis = Politician.objects.all().order_by('hg_name')
    

    #페이징 작업 위함
    paginated_by = 10
    total_count = len(polis)
    total_page = math.ceil(total_count/paginated_by)
    initial=((page-1)//10)*10+1
    next_end = initial+10
    if (next_end>total_page):
        next_end = total_page+1
    page_range = range(initial, next_end)
    if (initial==1):
        before_end = 1
    else:
        before_end = next_end-12
    start_index = paginated_by * (page-1)
    end_index = paginated_by * page
    polis = polis[start_index:end_index]
    print(page)
    return render(request,'feedpage/search.html', {"polis":polis, 'total_page':total_page, 'page_range':page_range, 'initial':initial, 'next_end':next_end, 'before_end':before_end})


def politician(request, pid):
    politician = Politician.objects.get(id = pid)
    normalFeeds = politician.normalFeeds.all()
    laws =  Law.objects.filter(proposer = politician)
    # 더 좋은 방법이 뭘가
    smallFeeds = SmallFeed.objects.filter(normalFeed__in=normalFeeds)
    return render(request,'feedpage/politician.html', {'politician': politician ,'normalFeeds' : normalFeeds, 'smallFeeds':smallFeeds, 'laws':laws})

def normalFeed_debate(request, pid, nfid):
    politician = Politician.objects.get(id = pid)
    normalFeed = NormalFeed.objects.get(id = nfid)
    comments = normalFeed.comments.all()
    comments_to_comment = CommentToComment.objects.none()
    for c in comments:
        temp = c.ctc.all()
        comments_to_comment = comments_to_comment.union(temp)
    
    return render(request,'feedpage/debate.html', {'politician': politician ,'normalFeed' : normalFeed, 'comments' : comments, 'comments_to_comment' : comments_to_comment})

def normalFeed_debate_new_comment(request, pid, nfid):
    content = request.POST['content']
    author = request.user
    normalFeed = NormalFeed.objects.get(id = nfid)
    Comment.objects.create(content=content, author = author, normalFeed=normalFeed)
    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    return redirect(path)

def normalFeed_debate_new_CTC(request, pid, nfid, cid):
    content = request.POST['content']
    author = request.user
    comment = Comment.objects.get(id = cid)
    CommentToComment.objects.create(content = content, author = author, comment = comment)
    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    return redirect(path)



#======================================================
#UPDATE
def lawupdate(request):
    politicians = Politician.objects.all()
    lawobject = Law.objects.all()
    for poli in politicians:
        laws = lawParsing(poli.hg_name)
        if len(laws) == 1: #발의법률안이 0개인 의원의 경우
            print("발의안한개도 없음")
            print(poli.hg_name)
            continue
        elif len(laws) == 8: #발의법률안이 1개이거나, 발의 법률안이 8개인 경우
            try:#발의법률안 1개인 경우
                try:
                    Law.objects.create(committee=laws['COMMITTEE'],bill_name = laws['BILL_NAME'],proposer=Politician.objects.get(id=poli.id),proposer_etc=laws['PROPOSER'], propose_dt=laws['PROPOSE_DT'],detail_link=laws['DETAIL_LINK'],member_link=laws['MEMBER_LIST'])
                except:
                    Law.objects.create(bill_name = laws['BILL_NAME'],proposer=Politician.objects.get(id=poli.id),proposer_etc=laws['PROPOSER'], propose_dt=laws['PROPOSE_DT'],detail_link=laws['DETAIL_LINK'],member_link=laws['MEMBER_LIST'])
            except:
                for number in range(len(laws)):
                    print(len(laws))
                    print(poli.hg_name,number)
                    try:
                        Law.objects.create(committee=laws[number]['COMMITTEE'],bill_name = laws[number]['BILL_NAME'],proposer=Politician.objects.get(id=poli.id),proposer_etc=laws[number]['PROPOSER'], propose_dt=laws[number]['PROPOSE_DT'],detail_link=laws[number]['DETAIL_LINK'],member_link=laws[number]['MEMBER_LIST'])
                    except:
                        Law.objects.create(bill_name = laws[number]['BILL_NAME'],proposer=Politician.objects.get(id=poli.id),proposer_etc=laws[number]['PROPOSER'], propose_dt=laws[number]['PROPOSE_DT'],detail_link=laws[number]['DETAIL_LINK'],member_link=laws[number]['MEMBER_LIST'])


        else :#발의 법안 2개 이상인 경우
            for number in range(len(laws)):
                print(len(laws))
                print(poli.hg_name,number)
                try:
                    Law.objects.create(committee=laws[number]['COMMITTEE'],bill_name = laws[number]['BILL_NAME'],proposer=Politician.objects.get(id=poli.id),proposer_etc=laws[number]['PROPOSER'], propose_dt=laws[number]['PROPOSE_DT'],detail_link=laws[number]['DETAIL_LINK'],member_link=laws[number]['MEMBER_LIST'])
                except:
                    Law.objects.create(bill_name = laws[number]['BILL_NAME'],proposer=Politician.objects.get(id=poli.id),proposer_etc=laws[number]['PROPOSER'], propose_dt=laws[number]['PROPOSE_DT'],detail_link=laws[number]['DETAIL_LINK'],member_link=laws[number]['MEMBER_LIST'])

                #law = Law.objects.get(bill_name = laws[number]['BILL_NAME']
    return render(request, 'feedpage/lawsearch.html',{'laws':laws})



def normalFeed_debate_comment_edit(request, pid, nfid, cid):
    comment = Comment.objects.get(id = cid)
    content = request.POST['content']
    comment.content = content
    comment.updated_at = timezone.now()
    comment.save()
    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    return redirect(path)

def normalFeed_debate_ctc_edit(request, pid, nfid, cid, ctcid):
    ctc = CommentToComment.objects.get(id = ctcid)
    content = request.POST['content']
    ctc.content = content
    ctc.updated_at = timezone.now()
    ctc.save()
    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    return redirect(path)

#lIKE & DISLIKE

def normalFeed_debate_ctc_like(request, pid, nfid, cid,ctcid):
    ctc = CommentToComment.objects.get(id = ctcid)
    like_list = ctc.userlikectc_set.filter(user_id = request.user.id)
    dislike_list = ctc.userdislikectc_set.filter(user_id = request.user.id)
    dislike_count = dislike_list.count()

    if like_list.count() > 0 :
        ctc.userlikectc_set.get(user_id = request.user.id).delete()
    else :
        UserLikeCTC.objects.create(user_id = request.user.id, ctc_id = ctc.id)

    if dislike_list.count() > 0 :
        ctc.userdislikectc_set.get(user_id = request.user.id).delete()

    context = {
        'like_count': like_list.count(),
        'dislike_count': dislike_count
    }

    return JsonResponse(context)

def normalFeed_debate_ctc_dislike(request, pid, nfid, cid,ctcid):
    ctc = CommentToComment.objects.get(id = ctcid)
    like_list = ctc.userlikectc_set.filter(user_id = request.user.id)
    dislike_list = ctc.userdislikectc_set.filter(user_id = request.user.id)
    like_count = like_list.count()

    if dislike_list.count() > 0 :
        ctc.userdislikectc_set.get(user_id = request.user.id).delete()
    else :
        UserDislikeCTC.objects.create(user_id = request.user.id, ctc_id = ctc.id)

    if like_list.count() > 0 :
        ctc.userlikectc_set.get(user_id = request.user.id).delete()

    context = {
        'dislike_count': dislike_list.count(),
        'like_count' : like_count
    }


    return JsonResponse(context)


def smallFeed_like(request, pid, sfid, nfid):
    smallFeed = SmallFeed.objects.get(id = sfid)
    like_list = smallFeed.userlikesmallfeed_set.filter(user_id = request.user.id)
    dislike_list = smallFeed.userdislikesmallfeed_set.filter(user_id = request.user.id)
    dislike_count = dislike_list.count()
    if like_list.count() > 0 :
        smallFeed.userlikesmallfeed_set.get(user_id = request.user.id).delete()
    else :
        UserLikeSmallFeed.objects.create(user_id = request.user.id, smallFeed_id = smallFeed.id)

    if dislike_list.count() > 0 :
        smallFeed.userdislikesmallfeed_set.get(user_id = request.user.id).delete()

    context = {
        'like_count': like_list.count(),
        'dislike_count': dislike_count
    }

    return JsonResponse(context)

def smallFeed_dislike(request, pid, sfid, nfid):
    smallFeed = SmallFeed.objects.get(id = sfid)
    like_list = smallFeed.userlikesmallfeed_set.filter(user_id = request.user.id)
    dislike_list = smallFeed.userdislikesmallfeed_set.filter(user_id = request.user.id)
    like_count = like_list.count()
    
    if dislike_list.count() > 0 :
        smallFeed.userdislikesmallfeed_set.get(user_id = request.user.id).delete()
    else :
        UserDislikeSmallFeed.objects.create(user_id = request.user.id, smallFeed_id = smallFeed.id)

    if like_list.count() > 0 :
        smallFeed.userlikesmallfeed_set.get(user_id = request.user.id).delete()


    context = {
        'dislike_count': dislike_list.count(),
        'like_count' : like_count
    }


    return JsonResponse(context)


def normalFeed_like(request, pid, nfid):
    normalFeed = NormalFeed.objects.get(id = nfid)
    like_list = normalFeed.userlikenormalfeed_set.filter(user_id = request.user.id)
    dislike_list = normalFeed.userdislikenormalfeed_set.filter(user_id = request.user.id)
    dislike_count = dislike_list.count()
    if like_list.count() > 0:
        normalFeed.userlikenormalfeed_set.get(user_id = request.user.id).delete()
    else :
        UserLikeNormalFeed.objects.create(user_id = request.user.id, normalFeed_id = normalFeed.id)

    if dislike_list.count() > 0 :
        normalFeed.userdislikenormalfeed_set.get(user_id = request.user.id).delete()

    context = {
        'like_count': like_list.count(),
        'dislike_count': dislike_count
    }

    return JsonResponse(context)
    # path = os.path.join('/feeds/politician/', str(pid))
    # return redirect(path)

def normalFeed_dislike(request, pid, nfid):
    normalFeed = NormalFeed.objects.get(id = nfid)
    like_list = normalFeed.userlikenormalfeed_set.filter(user_id = request.user.id)
    dislike_list = normalFeed.userdislikenormalfeed_set.filter(user_id = request.user.id)
    like_count = like_list.count()

    if dislike_list.count() > 0 :
        normalFeed.userdislikenormalfeed_set.get(user_id = request.user.id).delete()
    else :
        UserDislikeNormalFeed.objects.create(user_id = request.user.id, normalFeed_id = normalFeed.id)

    if like_list.count() > 0 :
        normalFeed.userlikenormalfeed_set.get(user_id = request.user.id).delete()

    context = {
        'dislike_count': dislike_list.count(),
        'like_count' : like_count
    }


    return JsonResponse(context)


def normalFeed_debate_comment_like(request, pid, nfid, cid):
    comment = Comment.objects.get(id = cid)
    like_list = comment.userlikecomment_set.filter(user_id = request.user.id)
    dislike_list = comment.userdislikecomment_set.filter(user_id = request.user.id)
    dislike_count = dislike_list.count()

    if like_list.count() > 0 :
        comment.userlikecomment_set.get(user_id = request.user.id).delete()
    else :
        UserLikeComment.objects.create(user_id = request.user.id, comment_id = comment.id)

    if dislike_list.count() > 0 :
        comment.userdislikecomment_set.get(user_id = request.user.id).delete()

    context = {
        'like_count': like_list.count(),
        'dislike_count': dislike_count
    }

    return JsonResponse(context)

def normalFeed_debate_comment_dislike(request, pid, nfid, cid):
    comment = Comment.objects.get(id = cid)
    like_list = comment.userlikecomment_set.filter(user_id = request.user.id)
    dislike_list = comment.userdislikecomment_set.filter(user_id = request.user.id)
    like_count = like_list.count()

    if dislike_list.count() > 0 :
        comment.userdislikecomment_set.get(user_id = request.user.id).delete()
    else :
        UserDislikeComment.objects.create(user_id = request.user.id, comment_id = comment.id)

    if like_list.count() > 0 :
        comment.userlikecomment_set.get(user_id = request.user.id).delete()

    context = {
        'dislike_count': dislike_list.count(),
        'like_count' : like_count
    }
    return JsonResponse(context)


def lawsearch(request, page=1, lawkey=None):
    if lawkey == None:
        lawsearch_key = request.POST.get('lawsearch_key',None)
    else:
        lawsearch_key = lawkey
    print("lawsearch는",lawsearch_key)
    if lawsearch_key:
        #laws = get_list_or_404(Law, bill_name__contains=lawsearch_key)
        laws = Law.objects.all().order_by('-propose_dt').filter(bill_name__icontains = lawsearch_key)
    else:
        laws = Law.objects.all().order_by('-propose_dt')
    
    #paging 작업
    paginated_by = 10
    total_count = len(laws)
    total_page = math.ceil(total_count/paginated_by)
    initial=((page-1)//10)*10+1
    next_end = initial+10
    if (next_end>total_page): 
        next_end = total_page+1
    page_range = range(initial, next_end)
    if (initial==1):
        before_end = 1
    else:
        before_end = next_end-12
    start_index = paginated_by * (page-1)
    end_index = paginated_by * page
    laws = laws[start_index:end_index]
    return render(request, 'feedpage/lawsearch.html', {"laws":laws, 'lawsearch_keyword':lawsearch_key, 'total_page':total_page, 'page_range':page_range, 'initial':initial, 'next_end':next_end, 'before_end':before_end})

def law_like(request, pid, lid):
    law = Law.objects.get(id = lid)
    like_list = law.userlikelaw_set.filter(user_id = request.user.id)
    dislike_list = law.userdislikelaw_set.filter(user_id = request.user.id)
    dislike_count = dislike_list.count()
    if like_list.count() > 0:
        law.userlikelaw_set.get(user_id = request.user.id).delete()
    else :
        UserLikeLaw.objects.create(user_id = request.user.id, law_id = law.id)

    if dislike_list.count() > 0 :
        law.userdislikelaw_set.get(user_id = request.user.id).delete()
    context = {
        'like_count': like_list.count(),
        'dislike_count': dislike_count
    }

    return JsonResponse(context) 

def law_dislike(request, pid, lid):
    law = Law.objects.get(id = lid)
    like_list = law.userlikelaw_set.filter(user_id = request.user.id)
    dislike_list = law.userdislikelaw_set.filter(user_id = request.user.id)
    like_count = dislike_list.count()
    if dislike_list.count() > 0:
        law.userdislikelaw_set.get(user_id = request.user.id).delete()
    else :
        UserDislikeLaw.objects.create(user_id = request.user.id, law_id = law.id)

    if like_list.count() > 0 :
        law.userlikelaw_set.get(user_id = request.user.id).delete()

    context = {
        'dislike_count': dislike_list.count(),
        'like_count': like_count
    }

    return JsonResponse(context)
    
def orientationVote(request, pid, value):
    politician = Politician.objects.get(id = pid)
    numOfUsers = politician.orientationvote_set.count()
    total = politician.politicalOrientation * numOfUsers
    OrientationVote.objects.create(user_id = request.user.id, politician= politician, value = value)
    politician.politicalOrientation = (total+value-5) / (numOfUsers+1)
    politician.save()
    path = os.path.join('/feeds/politician/', str(pid))
    return redirect(path)
    


#=================================================================
#DELETE

#Delete Comment
def normalFeed_debate_comment_delete(request, pid, nfid, cid):
    comment = Comment.objects.get(id = cid).delete()
    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    return redirect(path)

def normalFeed_debate_ctc_delete(request, pid, nfid, cid, ctcid):
    ctc = CommentToComment.objects.get(id = ctcid).delete()
    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    return redirect(path)

def orientationVoteCancel(request,  pid):
    politician = Politician.objects.get(id = pid)
    numOfUsers = politician.orientationvote_set.count()
    total = politician.politicalOrientation * numOfUsers
    value = OrientationVote.objects.get(user_id = request.user.id, politician= politician).value
    if numOfUsers != 1:
        politician.politicalOrientation = (total - value) / (numOfUsers-1)
    else:
        politician.politicalOrientation = 0
    politician.save()
    OrientationVote.objects.get(user_id = request.user.id, politician= politician).delete()
    path = os.path.join('/feeds/politician/', str(pid))
    return redirect(path)






    politician = Politician.objects.get(id = pid)
    numOfUsers = politician.orientationvote_set.count()
    total = politician.politicalOrientation * numOfUsers
    value = OrientationVote.objects.get(user_id = request.user.id, politician= politician).value
    if numOfUsers != 1:
        politician.politicalOrientation = (total - value) / (numOfUsers-1)
    else:
        politician.politicalOrientation = 0
    politician.save()
    OrientationVote.objects.get(user_id = request.user.id, politician= politician).delete()
    path = os.path.join('/feeds/politician/', str(pid))
    return redirect(path)






