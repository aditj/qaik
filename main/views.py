from django.http import request,HttpResponse
from django.shortcuts import render,redirect
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
import re
from django.contrib.auth.models import User
from django.contrib import messages #import messages
from .models import QAIT,UserProfile,Hashtag, Like,Reply,Following
from django.contrib.auth.hashers import make_password
from django.db.models import Exists, OuterRef

@login_required
def feed(request):
	trends=Hashtag.objects.all()
	qaits = QAIT.objects.order_by('-date','-time')[:100]
	people=UserProfile.objects.order_by('?')[:5]
	return render(request,"main/feed.html",context={
		'feed_title':'Feed',
		'trends':trends,
		'qaits': qaits,
		'people':people,
	})

def login_view(request):
	if request.method=="POST":
		print(request.POST['username'],request.POST['password'])
		user=authenticate(username=request.POST['username'],password=request.POST['password'])
		print(user)
		if user is not None:
			login(request,user)

			return redirect("/feed")
		else:
			return redirect("/login")
	return render(request,"main/login.html")

def register(request):
	if request.method == "POST":
		user = User(username=request.POST['username'],password=make_password(request.POST['password']),email=request.POST['email'],first_name=request.POST['first_name'],last_name=request.POST['last_name'])
		user.save()
		p=UserProfile(user=user)
		p.save()
		login(request, user)
		messages.success(request, "Registration successful." )
		return redirect("/feed")
	

	return render (request=request, template_name="main/register.html")
def logout_view(request):
	logout(request)
	return redirect("/login")

def create_qait(request):
	hashtags=re.findall("#(\w+)",request.POST["content"])
	
	for h in hashtags:
		hashtag=Hashtag.objects.get_or_create(title=h)[0]

		hashtag.count= hashtag.count+1
		hashtag.save()
	p=UserProfile.objects.filter(user=request.user).first()
	
	q=QAIT(content=request.POST["content"],by=p,by_id=p.id)

	q.save()
	return redirect('/feed')
def profile(request,user):
	user=UserProfile.objects.get(user=User.objects.get(username=user))
	qaits=QAIT.objects.filter(by=user)
	followers=Following.objects.filter(following=user)
	following=Following.objects.filter(follower=user)
	
	return render(request,"main/profile.html",context={'user':user,'followers':followers,'following':following,'qaits':qaits})


def like_dislike(request):
	q=QAIT.objects.get(id=request.POST['postId'])
	p=UserProfile.objects.get(user=User.objects.get(username=request.POST['likedBy']))

	
	l,created=Like.objects.get_or_create(qait=q,liker=p)

	if(not created):
		l.delete()
	else:
		l.save()
	c=Like.objects.filter(qait=q).count()
	return HttpResponse(c)
def reply(request):
	
	q=QAIT.objects.get(id=request.POST['reply_to'])
	content=request.POST['content']
	p=UserProfile.objects.get(user=User.objects.get(username=request.user))
	r,created=Reply.objects.get_or_create(content=content,by=p,reply_to=q)

	if(not created):
		r.delete()
	else:
		r.save()
	c=Reply.objects.filter(reply_to=q).count()
	return HttpResponse(c)
def see_replies(request,qait_id):
	q=QAIT.objects.get(id=qait_id)
	trends=Hashtag.objects.all()
	qaits = Reply.objects.filter(reply_to=q)
	people=UserProfile.objects.order_by('?')[:5]
	return render(request,"main/feed.html",context={
		'feed_title':'Feed',
		'trends':trends,
		'qaits': qaits,
		'people':people,
	})
def create_following(request):
	following=UserProfile.objects.get(id=request.POST['person_id'])
	follower=UserProfile.objects.get(user=User.objects.get(username=request.user))
	f,created=Following.objects.get_or_create(follower=follower,following=following)
	if(not created):
		f.delete()
	else:
		f.save()
	return HttpResponse(created)
def search(request,query):
	qaits=QAIT.objects.filter(content__contains=query)
	trends=Hashtag.objects.all()
	people=UserProfile.objects.order_by('?')[:5]
	return render(request,"main/feed.html",context={
		'feed_title':'Search Results',
		'trends':trends,
		'qaits': qaits,
		'people':people,
	})