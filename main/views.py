from django.shortcuts import render,redirect
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
import re

from django.contrib import messages #import messages
from .models import QAIT,UserProfile,Hashtag
@login_required
def feed(request):
	trends=Hashtag.objects.all()
	return render(request,"main/feed.html",context={
		'trends':trends,
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
def logout_view(request):
	logout(request)
	return redirect("/login")
def create_qait(request):
	hashtags=re.findall("#(\w+)",request.POST["content"])
	for h in hashtags:
		hashtag=Hashtag.objects.get_or_create(title=h)
		hashtag.count= hashtag.count+1
		hashtag.save()
	p=UserProfile.objects.filter(user=request.user).first()
	
	q=QAIT(content=request.POST["content"],by=p)

	q.save()
	return redirect('/feed')