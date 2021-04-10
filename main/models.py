from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(User):
    # TODO add User Image
    bio=models.TextField(blank=True,default='')
    dob=models.DateField(blank=True,null=True)
    perc_objectionble=models.FloatField(default=0)
class QAIT(models.Model):
    content=models.CharField(max_length=140)
    by=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_created=True)
    time=models.TimeField(auto_created=True)
    perc_objectionble=models.FloatField(default=0)
class Reply(QAIT):
    reply_to=models.ForeignKey(QAIT,on_delete=models.CASCADE,related_name="parent_qait")
class Like(models.Model):
    qait=models.ForeignKey(QAIT,on_delete=models.CASCADE)
    liker=models.ForeignKey(User,on_delete=models.CASCADE)

class Following(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    following= models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")

class Hashtag(models.Model):
    title=models.CharField(max_length=50)
    count=models.IntegerField(default=0)
class HashtagTweets(models.Model):
    hashtag=models.ForeignKey(Hashtag,on_delete=models.CASCADE)
    person=models.ForeignKey(User,on_delete=models.CASCADE)
