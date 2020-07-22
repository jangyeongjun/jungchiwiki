from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
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
    link = models.TextField() #이게 맞나??

    # 1:N, M:N
    like_users             = models.ManyToManyField(User, blank=True, related_name = 'like_law',             through='UserLikeLaw')
    dislike_users          = models.ManyToManyField(User, blank=True, related_name = 'dislike_law',          through='UserDislikeLaw' )
    comment_users          = models.ManyToManyField(User, blank=True, related_name = 'comment_law',          through='UserCommentLaw')


# 국회의원 모델
class Politician(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    genderChoices = [
        ('남', 'man'),
        ('여', 'woman'),
    ]
    gender = models.CharField(max_length=1, choices=genderChoices)
    district = models.CharField(max_length=10)
    politicalParty = models.CharField(max_length=20) #이것도 choice로 고르게
    politicalCommittee = models.CharField(max_length=20)
    #사진 추가+
    politicalOrientation = models.IntegerField()
    electedCount = models.IntegerField() #17대, 19대, 21대 이렇게 보여주려면 어떻게 저장해야하지
    
    #1:N, M:N
    like_users             = models.ManyToManyField(User, blank=True, related_name = 'like_politican',             through='UserLikePolitican')
    dislike_users          = models.ManyToManyField(User, blank=True, related_name = 'dislike_politican',          through='UserDislikePolitican' )
    orientation_vote_users = models.ManyToManyField(User, blank=True, related_name = 'orientation_vote_politican', through='OrientationVote')
    like_law               = models.ManyToManyField(Law,  blank=True, related_name = 'like_politican',             through='PoliticanLikeLaw')
    dislike_law            = models.ManyToManyField(Law,  blank=True, related_name = 'dislike_politican',          through='PoliticanDislikeLaw')
    abstain_law            = models.ManyToManyField(Law,  blank=True, related_name = 'abstain_politican',          through='PoliticanAbstainLaw')
    propose_law            = models.ManyToManyField(Law,  blank=True, related_name = 'propose_politican',          through='PoliticanProposeLaw')



#Law relate 해주는 model들
class UserLikeLaw(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    law = models.ForeignKey(Law, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class UserDislikeLaw(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    law = models.ForeignKey(Law, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class UserCommentLaw(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    law = models.ForeignKey(Law, on_delete = models.CASCADE)
    content = models.TextField()
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
    politican = models.ForeignKey(Politician, on_delete = models.CASCADE)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)

class PoliticanLikeLaw(models.Model):
    law = models.ForeignKey(Law, on_delete = models.CASCADE)
    politican = models.ForeignKey(Politician, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

class PoliticanDislikeLaw(models.Model):
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




class Comment(models.Model):
    content = models.TextField()
    created_at = models.CharField(max_length=10)
    #사진 혹은 통계자료
    evaluationChoices = [
        ('이행', 'implemented'),
        ('미흡', 'inadequate'),
        ('불이행', 'failure')
    ]
    evaluation = models.CharField(max_length = 3, choices = evaluationChoices)