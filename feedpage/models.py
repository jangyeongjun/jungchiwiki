from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Feedpage에 만들어야 할 모델
# 1. 국회의원
# 2. 법률
# 3. 평범 피드
# 4. 소항목
# 5. 댓글
# 6. 싫어요
# 7. 좋아요

#법안 모델



class Law(models.Model):
    name = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.CharField(max_length=10)
    link = models.URLField() #link는 URLS

    # 1:N, M:N
    like_users             = models.ManyToManyField(User, blank=True, related_name = 'like_law',             through='UserLikeLaw')
    dislike_users          = models.ManyToManyField(User, blank=True, related_name = 'dislike_law',          through='UserDislikeLaw' )
    



#국회의원 모델
class Politician(models.Model):
    name = models.CharField(max_length=10)
    PartyChoices = [
        ('더불어민주당', '더불어민주당'),
        ('미래통합당', '미래통합당'),
        ('정의당', '정의당'),
        ('국민의당', '국민의당'),
        ('열린민주당', '열린민주당'),
        ('기본소득당', '기본소득당'),
        ('시대전환', '시대전환'),
        ('무소속', '무소속'),
    ]
    politicalParty = models.CharField(max_length=10, choices=PartyChoices)
    politicalCommittee = models.CharField(max_length=20)
    district = models.CharField(max_length=30)
    genderChoices = [
        ('남', '남자'),
        ('여', '여자'),
    ]#첫번째 요소가 모델에 저장될 값, 두번째 요소가 사람이 읽을 값
    gender = models.CharField(max_length=2, choices=genderChoices)
    countChoices = [
        ('초선', '초선'),
        ('재선', '재선'),
        ('3선', '3선'),
        ('4선', '4선'),
        ('5선', '5선'),
        ('6선', '6선'),
        ('7선', '7선'),
        ('8선', '8선'),
        ('9선', '9선'),
        ('10선', '10선'),
    ]
    electedCount = models.CharField(max_length=10,blank=True, choices=genderChoices)
    howChoices = [
        ('지역구', '지역구'),
        ('비례대표', '비례대표'),
    ]
    how = models.CharField(max_length=20,blank=True)
    photo = models.ImageField(blank=True)
    age = models.IntegerField(default=0,blank=True)
    politicalOrientation = models.IntegerField(default=0,blank=True)
    # electedCount = models.CommaSeparatedIntegerField(max_length=20)
    # feedpage.Politician.electedCount: (fields.E901) CommaSeparatedIntegerField is removed except for support in historical migrations.
        # HINT: Use CharField(validators=[validate_comma_separated_integer_list]) instead.
    
    #M:N
    like_users             = models.ManyToManyField(User, blank=True, related_name = 'like_politican',             through='UserLikePolitican')
    dislike_users          = models.ManyToManyField(User, blank=True, related_name = 'dislike_politican',          through='UserDislikePolitican' )
    orientation_vote_users = models.ManyToManyField(User, blank=True, related_name = 'orientation_vote_politican', through='OrientationVote')
    agree_law              = models.ManyToManyField(Law,  blank=True, related_name = 'agree_politican',            through='PoliticanAgreeLaw')
    disagree_law           = models.ManyToManyField(Law,  blank=True, related_name = 'disagree_politican',         through='PoliticanDisagreeLaw')
    abstain_law            = models.ManyToManyField(Law,  blank=True, related_name = 'abstain_politican',          through='PoliticanAbstainLaw')
    propose_law            = models.ManyToManyField(Law,  blank=True, related_name = 'propose_politican',          through='PoliticanProposeLaw')

#normal_feed
class NormalFeed(models.Model):
    titleChoices = [
        ('1', '개요'),
        ('2', '경력'),
        ('3', '과거 공약/이행률'),
        ('4', '발의 법률안'),
        ('5', '찬성/반대 법안'),
        ('6', '발언 및 논란'),
    ]

    title = models.CharField(max_length=256, choices=titleChoices)
    content = models.TextField()
    photo = models.ImageField(blank=True, upload_to='feed_photos')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

    #1:N
    author = models.ForeignKey(User, null=True, on_delete = models.PROTECT)
    politician = models.ForeignKey(Politician, null=True, on_delete = models.CASCADE, related_name='normalFeeds')
    
    #M:N
    like_users             = models.ManyToManyField(User, blank=True, related_name = 'like_normalFeed',             through='UserLikeNormalFeed')
    dislike_users          = models.ManyToManyField(User, blank=True, related_name = 'dislike_normalFeed',          through='UserDislikeNormalFeed' )



#small_feed
class SmallFeed(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    photo = models.ImageField(blank=True, upload_to='smallfeed_photos')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

    #1:N
    author = models.ForeignKey(User, null=True, on_delete = models.PROTECT)
    normalFeed = models.ForeignKey(NormalFeed,  null=True, on_delete = models.CASCADE, related_name='smallFeeds')
    #M:N
    like_users             = models.ManyToManyField(User, blank=True, related_name = 'like_smallFeed',             through='UserLikeSmallFeed')
    dislike_users          = models.ManyToManyField(User, blank=True, related_name = 'dislike_smallFeed',          through='UserDislikeSmallFeed' )


#reference_feed
class ReferenceFeed(models.Model):
    content = models.TextField()
    referenceUrl = models.URLField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

    #1:N
    author = models.ForeignKey(User, null=True, on_delete = models.PROTECT)
    #M:N
    like_users             = models.ManyToManyField(User, blank=True, related_name = 'like_reference',             through='UserLikeReference')
    dislike_users          = models.ManyToManyField(User, blank=True, related_name = 'dislike_reference',          through='UserDislikeReference' )


#댓글모델
class Comment(models.Model):
    content = models.TextField()
    created_at = models.CharField(max_length=35, default=timezone.now)
    photo = models.ImageField(blank=True, upload_to='comment_photos')
    evaluationChoices = [
        ('이행', 'implemented'),
        ('미흡', 'inadequate'),
        ('불이행', 'failure')
    ]
    evaluation = models.CharField(max_length = 35, choices = evaluationChoices, blank=True)#일반토론인 경우에는 blank값
    #1:N
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT) #유저가 사라져도 댓글은 사라지지 않음
    law = models.ForeignKey(Law, blank=True,  null=True, on_delete=models.CASCADE)
    normalFeed = models.ForeignKey(NormalFeed, blank=True, null=True, on_delete=models.CASCADE, related_name = 'comments')
    smallFeed = models.ForeignKey(SmallFeed,blank=True,  null=True, on_delete=models.CASCADE, related_name = 'comments')
    politician = models.ForeignKey(Politician, blank=True,  null=True, on_delete=models.CASCADE, related_name = 'comments')
    
    #N:M
    like_users             = models.ManyToManyField(User, blank=True, related_name = 'like_comment',             through='UserLikeComment')
    dislike_users          = models.ManyToManyField(User, blank=True, related_name = 'dislike_comment',          through='UserDislikeComment' )
    # politician             = models.ManyToManyField(User, blank=True, related_name = 'comment',                  through='CommentToPolitican' )
    # 하나의 댓글은 한 명의 정치인한테 달리고 한 명의 정치인한테 여러 개 댓글이 달릴 수 있으니까 위에 law 처럼 1:N인듯??? 


#대댓글 모델
class CommentToComment(models.Model):
    content = models.TextField()
    created_at = models.CharField(max_length=36, default=timezone.now)
    photo = models.ImageField(blank=True, upload_to='comment_photos')
    #1:N
    author = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="ctc")
    #N:M
    like_users             = models.ManyToManyField(User, blank=True, related_name = 'like_CTC',             through='UserLikeCTC')
    dislike_users          = models.ManyToManyField(User, blank=True, related_name = 'dislike_CTC',          through='UserDislikeCTC' )










#Law relate 해주는 model들
class UserLikeLaw(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    law = models.ForeignKey(Law, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class UserDislikeLaw(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    law = models.ForeignKey(Law, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)


    

#politican relate 해주는 model들
class UserLikePolitican(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    politican = models.ForeignKey(Politician, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class UserDislikePolitican(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    politican = models.ForeignKey(Politician, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class OrientationVote(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    politician = models.ForeignKey(Politician, on_delete = models.CASCADE)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)

class PoliticanAgreeLaw(models.Model):
    law = models.ForeignKey(Law, on_delete = models.CASCADE)
    politican = models.ForeignKey(Politician, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class PoliticanDisagreeLaw(models.Model):
    law = models.ForeignKey(Law, on_delete = models.CASCADE)
    politican = models.ForeignKey(Politician, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class PoliticanAbstainLaw(models.Model):
    law = models.ForeignKey(Law, on_delete = models.CASCADE)
    politican = models.ForeignKey(Politician, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class PoliticanProposeLaw(models.Model):
    law = models.ForeignKey(Law, on_delete = models.CASCADE)
    politican = models.ForeignKey(Politician, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

#normal_feed relate
class UserLikeNormalFeed(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    normalFeed = models.ForeignKey(NormalFeed, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class UserDislikeNormalFeed(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    normalFeed = models.ForeignKey(NormalFeed, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)


#small_feed relate
class UserLikeSmallFeed(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    smallFeed = models.ForeignKey(SmallFeed, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class UserDislikeSmallFeed(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    smallFeed = models.ForeignKey(SmallFeed, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

#Reference_feed relate
class UserLikeReference(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    reference = models.ForeignKey(ReferenceFeed, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class UserDislikeReference(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    reference = models.ForeignKey(ReferenceFeed, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

#Comment relate
class UserLikeComment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class UserDislikeComment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

# class CommentToPolitician(models.Model):
#     politician = models.ForeignKey(Politician, on_delete = models.CASCADE)
#     comment = models.ForeignKey(Comment, on_delete = models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add = True)

#CTC relate
class UserLikeCTC(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    ctc = models.ForeignKey(CommentToComment, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class UserDislikeCTC(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    ctc = models.ForeignKey(CommentToComment, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)