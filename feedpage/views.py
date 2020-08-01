from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import *
from .crawling import lawParsing
from .crawling import poliParsing
import os
from django.http import JsonResponse
# Create your views here.
def main(request):
    politicians = Politician.objects.all()
    return render(request,'feedpage/main.html', {'politicians' : politicians})
 
def search(request):
    return render(request,'feedpage/search.html')


def politician(request, pid):
    politician = Politician.objects.get(id = pid)
    normalFeeds = politician.normalFeeds.all()
    # 더 좋은 방법이 뭘가
    smallFeeds = SmallFeed.objects.filter(normalFeed__in=normalFeeds)
    return render(request,'feedpage/politician.html', {'politician': politician ,'normalFeeds' : normalFeeds, 'smallFeeds':smallFeeds})

def orientationVote(request, pid, value):
    politician = Politician.objects.get(id = pid)
    numOfUsers = politician.orientationvote_set.count()
    total = politician.politicalOrientation * numOfUsers
    OrientationVote.objects.create(user_id = request.user.id, politician= politician, value = value)
    politician.politicalOrientation = (total+value-5) / (numOfUsers+1)
    politician.save()
    path = os.path.join('/feeds/politician/', str(pid))
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


def smallFeed_like(request, pid, sfid, nfid):
    smallFeed = SmallFeed.objects.get(id = sfid)
    like_list = smallFeed.userlikesmallfeed_set.filter(user_id = request.user.id)
    dislike_list = smallFeed.userdislikesmallfeed_set.filter(user_id = request.user.id)

    if like_list.count() > 0 :
        smallFeed.userlikesmallfeed_set.get(user_id = request.user.id).delete()
    else :
        UserLikeSmallFeed.objects.create(user_id = request.user.id, smallFeed_id = smallFeed.id)

    if dislike_list.count() > 0 :
        smallFeed.userdislikesmallfeed_set.get(user_id = request.user.id).delete()

    path = os.path.join('/feeds/politician/', str(pid))
    return redirect(path)

def smallFeed_dislike(request, pid, sfid, nfid):
    smallFeed = SmallFeed.objects.get(id = sfid)
    like_list = smallFeed.userlikesmallfeed_set.filter(user_id = request.user.id)
    dislike_list = smallFeed.userdislikesmallfeed_set.filter(user_id = request.user.id)

    if dislike_list.count() > 0 :
        smallFeed.userdislikesmallfeed_set.get(user_id = request.user.id).delete()
    else :
        UserDislikeSmallFeed.objects.create(user_id = request.user.id, smallFeed_id = smallFeed.id)

    if like_list.count() > 0 :
        smallFeed.userlikesmallfeed_set.get(user_id = request.user.id).delete()


    path = os.path.join('/feeds/politician/', str(pid))
    return redirect(path)


def normalFeed_like(request, pid, nfid):
    politician = Politician.objects.get(id = pid)
    normalFeed = NormalFeed.objects.get(id = nfid)
    like_list = normalFeed.userlikenormalfeed_set.filter(user_id = request.user.id)
    dislike_list = normalFeed.userdislikenormalfeed_set.filter(user_id = request.user.id)

    if like_list.count() > 0:
        normalFeed.userlikenormalfeed_set.get(user_id = request.user.id).delete()
    else :
        UserLikeNormalFeed.objects.create(user_id = request.user.id, normalFeed_id = normalFeed.id)

    if dislike_list.count() > 0 :
        normalFeed.userdislikenormalfeed_set.get(user_id = request.user.id).delete()

    context = {
        'pid' : politician.id,
        'nfid': normalFeed.id,
        'like_count': like_list.count()
    }

    return JsonResponse(context)
    # path = os.path.join('/feeds/politician/', str(pid))
    # return redirect(path)

def normalFeed_dislike(request, pid, nfid):
    normalFeed = NormalFeed.objects.get(id = nfid)
    like_list = normalFeed.userlikenormalfeed_set.filter(user_id = request.user.id)
    dislike_list = normalFeed.userdislikenormalfeed_set.filter(user_id = request.user.id)

    if dislike_list.count() > 0 :
        normalFeed.userdislikenormalfeed_set.get(user_id = request.user.id).delete()
    else :
        UserDislikeNormalFeed.objects.create(user_id = request.user.id, normalFeed_id = normalFeed.id)

    if like_list.count() > 0 :
        normalFeed.userlikenormalfeed_set.get(user_id = request.user.id).delete()

    context = {
        'dislike_count': dislike_list.count()
    }


    return JsonResponse(context)


def normalFeed_comment_like(request, pid, nfid, cid):
    comment = Comment.objects.get(id = cid)
    like_list = comment.userlikecomment_set.filter(user_id = request.user.id)
    dislike_list = comment.userdislikecomment_set.filter(user_id = request.user.id)

    if like_list.count() > 0 :
        comment.userlikecomment_set.get(user_id = request.user.id).delete()
    else :
        UserLikeComment.objects.create(user_id = request.user.id, comment_id = comment.id)

    if dislike_list.count() > 0 :
        comment.userdislikecomment_set.get(user_id = request.user.id).delete()

    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    
    return redirect(path)

def normalFeed_comment_dislike(request, pid, nfid, cid):
    comment = Comment.objects.get(id = cid)
    like_list = comment.userlikecomment_set.filter(user_id = request.user.id)
    dislike_list = comment.userdislikecomment_set.filter(user_id = request.user.id)

    if dislike_list.count() > 0 :
        comment.userdislikecomment_set.get(user_id = request.user.id).delete()
    else :
        UserDislikeComment.objects.create(user_id = request.user.id, comment_id = comment.id)

    if like_list.count() > 0 :
        comment.userlikecomment_set.get(user_id = request.user.id).delete()

    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    return redirect(path)

def lawsearch(request):
    return render(request, 'feedpage/lawsearch.html')

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
                    Law.objects.create(committee=laws['COMMITTEE'],bill_name = laws['BILL_NAME'],proposer=Politician.objects.get(id=poli.id),proposer_etc=laws['PROPOSER'], propse_dt=laws['PROPOSE_DT'],detail_link=laws['DETAIL_LINK'],member_link=laws['MEMBER_LIST'])
                except:
                    Law.objects.create(bill_name = laws['BILL_NAME'],proposer=Politician.objects.get(id=poli.id),proposer_etc=laws['PROPOSER'], propse_dt=laws['PROPOSE_DT'],detail_link=laws['DETAIL_LINK'],member_link=laws['MEMBER_LIST'])
            except:
                for number in range(len(laws)):
                    print(len(laws))
                    print(poli.hg_name,number)
                    try:
                        Law.objects.create(committee=laws[number]['COMMITTEE'],bill_name = laws[number]['BILL_NAME'],proposer=Politician.objects.get(id=poli.id),proposer_etc=laws[number]['PROPOSER'], propse_dt=laws[number]['PROPOSE_DT'],detail_link=laws[number]['DETAIL_LINK'],member_link=laws[number]['MEMBER_LIST'])
                    except:
                        Law.objects.create(bill_name = laws[number]['BILL_NAME'],proposer=Politician.objects.get(id=poli.id),proposer_etc=laws[number]['PROPOSER'], propse_dt=laws[number]['PROPOSE_DT'],detail_link=laws[number]['DETAIL_LINK'],member_link=laws[number]['MEMBER_LIST'])


        else :
            for number in range(len(laws)):
                print(len(laws))
                print(poli.hg_name,number)
                try:
                    Law.objects.create(committee=laws[number]['COMMITTEE'],bill_name = laws[number]['BILL_NAME'],proposer=Politician.objects.get(id=poli.id),proposer_etc=laws[number]['PROPOSER'], propse_dt=laws[number]['PROPOSE_DT'],detail_link=laws[number]['DETAIL_LINK'],member_link=laws[number]['MEMBER_LIST'])
                except:
                    Law.objects.create(bill_name = laws[number]['BILL_NAME'],proposer=Politician.objects.get(id=poli.id),proposer_etc=laws[number]['PROPOSER'], propse_dt=laws[number]['PROPOSE_DT'],detail_link=laws[number]['DETAIL_LINK'],member_link=laws[number]['MEMBER_LIST'])

                #law = Law.objects.get(bill_name = laws[number]['BILL_NAME']
    return render(request, 'feedpage/lawsearch.html',{'laws':laws})

def polisearch(request):
    polis = poliParsing()
    for number in range(len(polis)):
        print(number)
        Politician.objects.create(hg_name = polis[number]['HG_NM'], eng_name = polis[number]['ENG_NM'], bth_name=polis[number]['BTH_GBN_NM'], bth_date=polis[number]['BTH_DATE'], job_res_name = polis[number]['JOB_RES_NM'], politicalParty = polis[number]['POLY_NM'], district = polis[number]['ORIG_NM'], politicalCommittee = polis[number]['CMITS'], electedCount = polis[number]['REELE_GBN_NM'], units = polis[number]['UNITS'], gender = polis[number]['SEX_GBN_NM'], tel_num = polis[number]['TEL_NO'], e_mail = polis[number]['E_MAIL'], homepage = polis[number]['HOMEPAGE'])
    return render(request,'feedpage/search.html')


def normalFeed_ctc_like(request, pid, nfid, cid,ctcid):
    ctc = CommentToComment.objects.get(id = ctcid)
    like_list = ctc.userlikectc_set.filter(user_id = request.user.id)
    dislike_list = ctc.userdislikectc_set.filter(user_id = request.user.id)

    if like_list.count() > 0 :
        ctc.userlikectc_set.get(user_id = request.user.id).delete()
    else :
        UserLikeCTC.objects.create(user_id = request.user.id, ctc_id = ctc.id)

    if dislike_list.count() > 0 :
        ctc.userdislikectc_set.get(user_id = request.user.id).delete()

    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    
    return redirect(path)


def normalFeed_ctc_dislike(request, pid, nfid, cid,ctcid):
    ctc = CommentToComment.objects.get(id = ctcid)
    like_list = ctc.userlikectc_set.filter(user_id = request.user.id)
    dislike_list = ctc.userdislikectc_set.filter(user_id = request.user.id)

    if dislike_list.count() > 0 :
        ctc.userdislikectc_set.get(user_id = request.user.id).delete()
    else :
        UserDislikeCTC.objects.create(user_id = request.user.id, ctc_id = ctc.id)

    if like_list.count() > 0 :
        ctc.userlikectc_set.get(user_id = request.user.id).delete()

    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    
    return redirect(path)
