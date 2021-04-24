from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UserProfile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    bio=models.TextField(blank=True,default='')
    dob=models.DateField(blank=True,null=True)
    perc_objectionble=models.FloatField(default=0)

class QAIT(models.Model):
    content=models.CharField(max_length=140)
    by=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    date=models.DateField(auto_created=True,auto_now_add=True)
    time=models.TimeField(auto_created=True,auto_now_add=True)
    perc_objectionble=models.FloatField(default=0)
    def get_like_no(self):
        return Like.objects.filter(qait=self).count()

class Reply(QAIT):
    reply_to=models.ForeignKey(QAIT,on_delete=models.CASCADE,related_name="parent_qait")

class Like(models.Model):
    qait=models.ForeignKey(QAIT,on_delete=models.CASCADE)
    liker=models.ForeignKey(UserProfile,on_delete=models.CASCADE)

class Following(models.Model):
    follower=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="follower")
    following= models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="following")

class Hashtag(models.Model):
    title=models.CharField(max_length=50)
    count=models.IntegerField(default=0)

class HashtagTweets(models.Model):
    hashtag=models.ForeignKey(Hashtag,on_delete=models.CASCADE)
    associated_qait=models.ForeignKey(QAIT,on_delete=models.CASCADE)
    
