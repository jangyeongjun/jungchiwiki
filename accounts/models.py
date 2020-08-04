from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  
from django.db.models.signals import post_save 
from django.dispatch import receiver  
from django.core.validators import MaxValueValidator, MinValueValidator

class Profile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, blank=True)
    genderChoices = [
        ('M', '남성'),
        ('F', '여성'),
    ]#튜플의 첫번째 요소가 저장될 값, 두번째 요소가 사람이 읽을 수 있는 이름
    gender = models.CharField(max_length=1, choices=genderChoices, blank=True)
    politicalOrientation = models.IntegerField(default=5, validators=[MaxValueValidator(10), MinValueValidator(0)])
    birth_dt = models.DateTimeField(blank=True,null = True)


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):  
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):  
        instance.profile.save()