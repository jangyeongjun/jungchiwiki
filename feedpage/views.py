from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import *
import os

# Create your views here.
def main(request):
    return render(request,'feedpage/main.html')
 
def search(request):
    return render(request,'feedpage/search.html')


def politician(request, pid):
    politician = Politician.objects.get(id = pid)
    normalFeeds = politician.normalFeeds.all()
    # 더 좋은 방법이 뭘가
    smallFeeds = SmallFeed.objects.filter(normalFeed__in=normalFeeds)
    
    

    return render(request,'feedpage/politician.html', {'politician': politician ,'normalFeeds' : normalFeeds, 'smallFeeds':smallFeeds})


def normalFeed_debate(request, pid, nfid):
    politician = Politician.objects.get(id = pid)
    normalFeed = NormalFeed.objects.get(id = nfid)
    comments = normalFeed.comments.all()
    return render(request,'feedpage/debate.html', {'politician': politician ,'normalFeed' : normalFeed, 'comments' : comments})


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
    normalFeed = NormalFeed.objects.get(id = nfid)
    like_list = normalFeed.userlikenormalfeed_set.filter(user_id = request.user.id)
    dislike_list = normalFeed.userdislikenormalfeed_set.filter(user_id = request.user.id)

    if like_list.count() > 0:
        normalFeed.userlikenormalfeed_set.get(user_id = request.user.id).delete()
    else :
        UserLikeNormalFeed.objects.create(user_id = request.user.id, normalFeed_id = normalFeed.id)

    if dislike_list.count() > 0 :
        normalFeed.userdislikenormalfeed_set.get(user_id = request.user.id).delete()

    path = os.path.join('/feeds/politician/', str(pid))
    return redirect(path)


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

    path = os.path.join('/feeds/politician/', str(pid))
    return redirect(path)



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