from django.http import request
from django.shortcuts import render,redirect
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
import re
from django.contrib.auth.models import User
from django.contrib import messages #import messages
from .models import QAIT,UserProfile,Hashtag, Like

@login_required
def feed(request):
	trends=Hashtag.objects.all()
<<<<<<< HEAD

=======
	qaits = QAIT.objects.all()
>>>>>>> d45dfe58a9fff634e122b3f85583b2c0e8a6498b
	return render(request,"main/feed.html",context={
		'trends':trends,
		'qaits': qaits,
	})

def login_view(request):
	if request.method=="POST":
		user=authenticate(username=request.POST['username'],password=request.POST['password'])
		if user is not None:
			login(request,user)
			return redirect("/feed")
		else:
			return redirect("/login")
	return render(request,"main/login.html")

def register(request):
	if request.method == "POST":
<<<<<<< HEAD
		user = User(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'],first_name=request.POST['first_name'],last_name=request.POST['last_name'])
		user.save()
		p=UserProfile(user=user)
		p.save()
		login(request, user)
		messages.success(request, "Registration successful." )
		return redirect("/feed")
	

	return render (request=request, template_name="main/register.html")
=======
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			p=UserProfile(user=user)
			p.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/feed")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="main/register.html", context={"register_form":form})

>>>>>>> d45dfe58a9fff634e122b3f85583b2c0e8a6498b
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
<<<<<<< HEAD
def profile(request):
	return render(request,"main/profile.html")
=======


def like_dislike(request):
	inp = request.POST
	print(inp)
>>>>>>> d45dfe58a9fff634e122b3f85583b2c0e8a6498b
