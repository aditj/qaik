from django.shortcuts import render,redirect
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout


from django.contrib import messages #import messages
from .models import QAIT,Profile
@login_required
def feed(request):
    return render(request,"main/feed.html")
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
			Profile(username=user)
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
	p=Profile.objects.filter(username=request.user).first()
	print(request.user.profile)
	q=QAIT(content=request.POST["content"],by=p)

	q.save()
	return redirect('/login')