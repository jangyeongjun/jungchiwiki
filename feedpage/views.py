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
import datetime


# Create your views here.

def main(request):
    party_list = [
        '더불어민주당', 
        '미래통합당', 
        '정의당',
        '국민의당',
        '열린민주당',
        '기본소득당',
        '시대전환',
        '무소속',
    ]
    politicians_by_party = []
    for party in party_list:
        politicians_by_party.append(Politician.objects.filter(politicalParty=party))


    politician_chosung = []
    chosung_list = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
    for politicians in politicians_by_party:
        list1 = []
        for ch in  chosung_list:
            list2 = []
            for politician in politicians:
                if politician.korean_chosung() == ch:
                    list2.append(politician)
            list1.append(list2)
        politician_chosung.append(list1)

    return render(request,'feedpage/main.html', {'politicians_by_party' : politicians_by_party, 'politician_chosung' : politician_chosung, 'chosung_list':chosung_list})



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

def normalFeed_debate_new_comment(request, pid, nfid):
    content = request.POST['content']
    value = request.POST['options']
    author = request.user
    normalFeed = NormalFeed.objects.get(id = nfid)
    time = str(datetime.datetime.now()).strip('.')[0:16]
    if value == '1':
        Comment.objects.create(content=content, 
                               author = author, 
                               normalFeed=normalFeed, 
                               likeChoice = 'like', 
                               created_at = time)
    elif value == '2':
        Comment.objects.create(content=content, 
                               author = author, 
                               normalFeed=normalFeed, 
                               likeChoice = 'dislike', 
                               created_at = time)
    
    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    return redirect(path)


def normalFeed_debate_new_CTC(request, pid, nfid, cid):
    content = request.POST['content']
    author = request.user
    comment = Comment.objects.get(id = cid)
    time = str(datetime.datetime.now()).strip('.')[0:16]
    CommentToComment.objects.create(content = content, author = author, comment = comment, created_at = time)
    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    return redirect(path)

def law_debate_new_comment(request, pid, lid):
    content = request.POST['content']
    value = request.POST['options']
    author = request.user
    law = Law.objects.get(id = lid)
    time = str(datetime.datetime.now()).strip('.')[0:16]
    if value =='1':
        Comment.objects.create(content=content, 
                               author = author, 
                               law=law, 
                               likeChoice='like', 
                               created_at = time )
    elif value == '2':
        Comment.objects.create(content=content, 
                               author = author, 
                               law=law, 
                               likeChoice='dislike', 
                               created_at = time )

    
    path = os.path.join('/feeds/politician', str(pid), 'law', str(lid), 'debate').replace("\\" , "/")
    return redirect(path)



def law_debate_new_CTC(request, pid, lid, cid):
    content = request.POST['content']
    author = request.user
    comment = Comment.objects.get(id = cid)
    CommentToComment.objects.create(content = content, author = author, comment = comment)
    path = os.path.join('/feeds/politician', str(pid), 'law', str(lid), 'debate').replace("\\" , "/")
    return redirect(path)





#===========================================================
#READ  
def polisearch(request):

    lawsearch_key = request.POST('lawseach_key')
    return render(request,'feedpage/search.html')




 
def search(request, page=1,poliname_v='x',poliparty_v='x',policommi_v='x',polidisstrict_v='x',poligender_v='x',polielected_v='x',polihow_v='x',poliori_v='x',poliAge_v='x',):

    #POST들어왔을 때, 캐치하기 위함
    if request.method == "POST":
        print(request.POST)
        #대조가 가능한 변수
        poliname_v        = request.POST["poliname"]
        poliparty_v       = request.POST["poliparty"]
        policommi_v       = request.POST["policommi"]
        polidisstrict_v   = request.POST["polidisstrict"]
        poligender_v      = request.POST["poligender"]
        polielected_v     = request.POST["polielected"]
        polihow_v         = request.POST["polihow"]
        #대조가 안되는 변수
        poliori_v         = request.POST["poliori"]
        poliAge_v         = request.POST["poliAge"]

        if polihow_v == '비례대표':
            polis = Politician.objects.all().order_by('hg_name').filter(
                hg_name__icontains              = poliname_v,
                politicalCommittee__icontains   = policommi_v,
                politicalParty__icontains       = poliparty_v,
                district__icontains             = polihow,
                gender__icontains               = poligender_v,
                electedCount__icontains         = polielected_v,
            )
        elif polihow_v == '지역구':
            polis = Politician.objects.all().order_by('hg_name').filter(
                hg_name__icontains              = poliname_v,
                politicalCommittee__icontains   = policommi_v,
                politicalParty__icontains       = poliparty_v,
                district__icontains             = polidisstrict_v,
                gender__icontains               = poligender_v,
                electedCount__icontains         = polielected_v,
            ).exclude(district='비례대표')
        else:
            polis = Politician.objects.all().order_by('hg_name').filter(
            hg_name__icontains              = poliname_v,
            politicalCommittee__icontains   = policommi_v,
            politicalParty__icontains       = poliparty_v,
            district__icontains             = polidisstrict_v,
            gender__icontains               = poligender_v,
            electedCount__icontains         = polielected_v
        )
        if poliori_v != '':
            if int(poliori_v) == 4:
                polis = polis.filter(politicalOrientation__gte=(int(poliori_v)))
            elif int(poliori_v)>=0:
                polis = polis.filter(politicalOrientation__gte=(int(poliori_v)),politicalOrientation__lt=(int(poliori_v)+1))
            elif int(poliori_v)==-5:
                polis = polis.filter(politicalOrientation__lte=(int(poliori_v)+1))
            else:
                polis = polis.filter(politicalOrientation__lte=(int(poliori_v)+1),politicalOrientation__gt=(int(poliori_v)))
        if poliAge_v != '':
            if int(poliAge_v) == 70:
                polis = polis.filter(age__gte=(int(poliAge_v)))
            elif int(poliAge_v) == 29:
                polis = polis.filter(age__lte=(int(poliAge_v)))
            else:
                polis = polis.filter(age__gte=(int(poliAge_v)),age__lt=(int(poliAge_v)+10))
            
        
        
    #검색했을 때, 검색 조건 유지 위함
    elif poliname_v !='x' or poliparty_v != 'x' or policommi_v !='x' or polidisstrict_v !='x' or poligender_v !='x' or polielected_v !='x' or polihow_v !='x' or poliori_v !='x' or poliAge_v !='x':
        if poliname_v =='x':
            poliname_v = ''
        if poliparty_v =='x':
            poliparty_v = ''
        if policommi_v =='x':
            policommi_v = ''
        if polidisstrict_v =='x':
            polidisstrict_v = ''
        if poligender_v =='x':
            poligender_v = ''
        if polielected_v =='x':
            polielected_v = ''
        if polihow_v =='x':
            polihow_v = ''
        if poliori_v =='x':
            poliori_v = ''
        if poliAge_v =='x':
            poliAge_v = ''
        

        if polihow_v == '비례대표':
            polis = Politician.objects.all().order_by('hg_name').filter(
                hg_name__icontains              = poliname_v,
                politicalCommittee__icontains   = policommi_v,
                politicalParty__icontains       = poliparty_v,
                district__icontains             = polihow,
                gender__icontains               = poligender_v,
                electedCount__icontains         = polielected_v,
            )
        elif polihow_v == '지역구':
            polis = Politician.objects.all().order_by('hg_name').filter(
                hg_name__icontains              = poliname_v,
                politicalCommittee__icontains   = policommi_v,
                politicalParty__icontains       = poliparty_v,
                district__icontains             = polidisstrict_v,
                gender__icontains               = poligender_v,
                electedCount__icontains         = polielected_v,
            ).exclude(district='비례대표')
        else:
            polis = Politician.objects.all().order_by('hg_name').filter(
            hg_name__icontains              = poliname_v,
            politicalCommittee__icontains   = policommi_v,
            politicalParty__icontains       = poliparty_v,
            district__icontains             = polidisstrict_v,
            gender__icontains               = poligender_v,
            electedCount__icontains         = polielected_v
        )
        print(poliori_v)
        if poliori_v != '':
            if int(poliori_v) == 4:
                polis = polis.filter(politicalOrientation__gte=(int(poliori_v)))
            elif int(poliori_v) >= 0:
                polis = polis.filter(politicalOrientation__gte=(int(poliori_v)),politicalOrientation__lt=(int(poliori_v)+1))
            elif int(poliori_v) == -5:
                polis = polis.filter(politicalOrientation__lte=(int(poliori_v)+1))
            else:
                polis = polis.filter(politicalOrientation__lte=(int(poliori_v)+1),politicalOrientation__gt=(int(poliori_v)))
        if poliAge_v != '':
            if int(poliAge_v) == 70:
                polis = polis.filter(age__gte=(int(poliAge_v)))
            elif int(poliAge_v) == 29:
                polis = polis.filter(age__lte=(int(poliAge_v)))
            else:
                polis = polis.filter(age__gte=(int(poliAge_v)),age__lt=(int(poliAge_v)+10))


    else:
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
    if poliname_v =='':
        poliname_v = 'x'
    if poliparty_v =='':
        poliparty_v = 'x'
    if policommi_v =='':
        policommi_v = 'x'
    if polidisstrict_v =='':
        polidisstrict_v = 'x'
    if poligender_v =='':
        poligender_v = 'x'
    if polielected_v =='':
        polielected_v = 'x'
    if polihow_v =='':
        polihow_v = 'x'
    if poliori_v =='':
        poliori_v = 'x'
    if poliAge_v =='':
        poliAge_v = 'x'
    return render(request,'feedpage/search.html', 
    {"polis":polis, 'total_page':total_page, 'page_range':page_range,
    'initial':initial, 'next_end':next_end, 'before_end':before_end,
    "poliname_v":poliname_v, "poliparty_v":poliparty_v, "policommi_v":policommi_v,
    "polidisstrict_v":polidisstrict_v, "poligender_v":poligender_v, "polielected_v":polielected_v,
    "polihow_v":polihow_v, "poliori_v":poliori_v,"poliAge_v":poliAge_v
    })


def lawsearch(request, page=1, lawkey='x'):

    if request.method == "POST":
        lawsearch_key = request.POST.get('lawsearch_key')
        laws = Law.objects.all().order_by('-propose_dt').filter(bill_name__icontains = lawsearch_key)
    elif lawkey != 'x':
        lawsearch_key = lawkey
        laws = Law.objects.all().order_by('-propose_dt').filter(bill_name__icontains = lawsearch_key)
        
    else:
        laws = Law.objects.all().order_by('-propose_dt')
        lawsearch_key = lawkey
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




def politician(request, pid):
    politician = Politician.objects.get(id = pid)
    normalFeeds = politician.normalFeeds.all().order_by('title')
    laws =  Law.objects.filter(proposer = politician)
    # 더 좋은 방법이 뭘가
    smallFeedsSet = []
    ranges = []

    for normalFeed in normalFeeds:
        smallFeeds = SmallFeed.objects.filter(normalFeed=normalFeed)
        smallFeedsSet.append(smallFeeds)
        ranges.append(range(smallFeeds.count()))

    return render(request,'feedpage/politician.html', {'politician': politician ,'normalFeeds' : normalFeeds, 'smallFeedsSet':smallFeedsSet, 'ranges':ranges, 'laws':laws})


def normalFeed_debate(request, pid, nfid):
    politician = Politician.objects.get(id = pid)
    laws =  Law.objects.filter(proposer = politician)
    normalFeed = NormalFeed.objects.get(id = nfid)
    like_comments = Comment.objects.filter(likeChoice='like', normalFeed=normalFeed)
    dislike_comments = Comment.objects.filter(likeChoice='dislike', normalFeed=normalFeed)
    
    comments_to_like_comment = CommentToComment.objects.none()
    comments_to_dislike_comment = CommentToComment.objects.none()
    for c in like_comments:
        temp = c.ctc.all()
        comments_to_like_comment = comments_to_like_comment.union(temp)
    for c in dislike_comments:
        temp = c.ctc.all()
        comments_to_dislike_comment = comments_to_dislike_comment.union(temp)
    
    return render(request,'feedpage/debate.html', {'politician': politician ,'normalFeed' : normalFeed, 'laws':laws, 'like_comments' : like_comments, 'dislike_comments' : dislike_comments, 'comments_to_like_comment' : comments_to_like_comment, 'comments_to_dislike_comment' : comments_to_dislike_comment})


def law_debate(request, pid, lid):

    politician = Politician.objects.get(id=pid)
    law = Law.objects.get(id = lid)
    comments = law.comments.all()
    
    like_comments = Comment.objects.filter(likeChoice='like', law=law)
    dislike_comments = Comment.objects.filter(likeChoice='dislike', law=law)
    
    comments_to_like_comment = CommentToComment.objects.none()
    comments_to_dislike_comment = CommentToComment.objects.none()
    for c in like_comments:
        temp = c.ctc.all()
        comments_to_like_comment = comments_to_like_comment.union(temp)
    for c in dislike_comments:
        temp = c.ctc.all()
        comments_to_dislike_comment = comments_to_dislike_comment.union(temp)
    
    
    return render(request,'feedpage/law_debate.html', {'politician':politician, 'law': law , 'like_comments' : like_comments, 'dislike_comments' : dislike_comments, 'comments_to_like_comment' : comments_to_like_comment, 'comments_to_dislike_comment' : comments_to_dislike_comment})
    




#======================================================
#UPDATE

def poliupdate(request):
    polis = poliParsing()
    currentPoliticians = Politician.objects.all()


    for number in range(len(polis)):
        print(polis[number]['HG_NM'])
        age_poli = 2020-int(polis[number]['BTH_DATE'][0:4])+1
        if currentPoliticians.filter(hg_name = polis[number]['HG_NM']):
            print(number)
        else :
            Politician.objects.create(hg_name = polis[number]['HG_NM'], eng_name = polis[number]['ENG_NM'], bth_name=polis[number]['BTH_GBN_NM'], bth_date=polis[number]['BTH_DATE'], job_res_name = polis[number]['JOB_RES_NM'], politicalParty = polis[number]['POLY_NM'], district = polis[number]['ORIG_NM'], politicalCommittee = polis[number]['CMITS'], electedCount = polis[number]['REELE_GBN_NM'], units = polis[number]['UNITS'], gender = polis[number]['SEX_GBN_NM'], tel_num = polis[number]['TEL_NO'], e_mail = polis[number]['E_MAIL'], homepage = polis[number]['HOMEPAGE'],age=age_poli)
    return render(request,'feedpage/search.html')


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


def normalFeed_edit(request, pid, nfid):
    normalFeed= NormalFeed.objects.get(id = nfid)
    content = request.POST['content']
    normalFeed.content = content
    normalFeed.updated_at = timezone.now()
    normalFeed.save()
    path = os.path.join('/feeds/politician', str(pid)).replace("\\" , "/")
    return redirect(path)

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


def smallFeed_edit(request, pid, nfid, sfid):
    smallFeed= SmallFeed.objects.get(id = sfid)
    content = request.POST['content']
    smallFeed.content = content
    smallFeed.updated_at = timezone.now()
    smallFeed.save()
    path = os.path.join('/feeds/politician', str(pid)).replace("\\" , "/")
    return redirect(path)

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


def normalFeed_debate_comment_edit(request, pid, nfid, cid):
    comment = Comment.objects.get(id = cid)
    content = request.POST['content']
    time = str(datetime.datetime.now()).strip('.')[0:16]
    comment.content = content
    comment.updated_at = time
    comment.save()
    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    return redirect(path)

def normalFeed_debate_ctc_edit(request, pid, nfid, cid, ctcid):
    ctc = CommentToComment.objects.get(id = ctcid)
    content = request.POST['content']
    time = str(datetime.datetime.now()).strip('.')[0:16]
    ctc.content = content
    ctc.updated_at = time
    ctc.save()
    path = os.path.join('/feeds/politician', str(pid), 'normalfeed', str(nfid), 'debate').replace("\\" , "/")
    return redirect(path)



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


def law_debate_comment_edit(request, pid, lid, cid):
    comment = Comment.objects.get(id = cid)
    content = request.POST['content']
    comment.content = content
    comment.updated_at = timezone.now()
    comment.save()
    path = os.path.join('/feeds/politician', str(pid), 'law', str(lid), 'debate').replace("\\" , "/")
    return redirect(path)

def law_debate_ctc_edit(request, pid, lid, cid, ctcid):
    ctc = CommentToComment.objects.get(id = ctcid)
    content = request.POST['content']
    ctc.content = content
    ctc.updated_at = timezone.now()
    ctc.save()
    path = os.path.join('/feeds/politician', str(pid), 'law', str(lid), 'debate').replace("\\" , "/")
    return redirect(path)



def law_debate_ctc_like(request, pid, lid, cid,ctcid):
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

def law_debate_ctc_dislike(request, pid, lid, cid,ctcid):
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


def law_debate_comment_like(request, pid, lid, cid):
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

def law_debate_comment_dislike(request, pid, lid, cid):
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
    like_count = like_list.count()
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

def law_debate_comment_delete(request, pid, lid, cid):
    comment = Comment.objects.get(id = cid).delete()
    path = os.path.join('/feeds/politician', str(pid), 'law', str(lid), 'debate').replace("\\" , "/")
    return redirect(path)

def law_debate_ctc_delete(request, pid, lid, cid, ctcid):
    ctc = CommentToComment.objects.get(id = ctcid).delete()
    path = os.path.join('/feeds/politician', str(pid), 'law', str(lid), 'debate').replace("\\" , "/")
    return redirect(path)

def normalFeed_delete(request, pid, nfid):
    normalFeed = NormalFeed.objects.get(id=nfid).delete()
    path = os.path.join('/feeds/politician', str(pid)).replace("\\" , "/")
    return redirect(path)

def smallFeed_delete(request, pid, nfid, sfid):
    smallFeed = SmallFeed.objects.get(id=sfid).delete()
    path = os.path.join('/feeds/politician', str(pid)).replace("\\" , "/")
    return redirect(path)


def orientationVoteCancel(request,  pid):
    politician = Politician.objects.get(id = pid)
    numOfUsers = politician.orientationvote_set.count()
    total = politician.politicalOrientation * numOfUsers
    value = OrientationVote.objects.get(user_id = request.user.id, politician= politician).value
    if numOfUsers != 1:
        politician.politicalOrientation = (total - value +5) / (numOfUsers-1)
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





#===================================================================================================
#information
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

def pie_chart(request, pid, nfid):
    normalFeed = NormalFeed.objects.get(id = nfid)
    like_m_num = len(normalFeed.like_users.filter(profile__gender = 'M'))
    like_f_num = len(normalFeed.like_users.filter(profile__gender = 'F'))
    print(like_m_num)
    print(like_f_num)
    labels = ['남성', '여성']
    data = [like_m_num,like_f_num]

    return render(request, 'feedpage/information.html', {
        'labels': labels,
        'data': data,
    })