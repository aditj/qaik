from typing import final
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
import networkx as nx
import pickle
import numpy as np
# from .preprocess_qait import *
from .classify import getPrediction
# ##### Hate Speech Detection #####

# def clean_qait(qait):
# 	return preprocess(qait)
# def flag_qait(qait):
# 	return getPrediction(qait)


##### Graph Related #####
def recommendor(Gr,curr_user,friends, k=3, alpha=0.7, rad = 3):
    connects = list(nx.ego_graph(Gr, curr_user, radius=rad, undirected=False).nodes)
    
    connects.remove(curr_user)
    connects = np.asarray(connects)
    node_pair = [(curr_user, node) for node in connects]
    users_score = np.zeros(len(node_pair))
    AAI = nx.adamic_adar_index(Gr,node_pair)
    AAI_score = np.asarray([nodescore[2] for nodescore in AAI],dtype=np.float64)
    final_score = AAI_score
    print(connects.shape==(0,))
    print(final_score)
    if(connects.shape==(0,)):
	    return np.asarray(UserProfile.objects.order_by('?').values_list('id', flat=True)[:k])
    for i , node in enumerate(connects):
        final_score+= np.log(len(final_score))/nx.shortest_path_length(Gr, curr_user,node)
        if node in friends:
            final_score[i]=0
    if np.min(final_score)==np.max(final_score):
        return np.random.choice(connects,replace=False, size = k)
    # Insted of just choosing the top k best matches., let us sample from the distribution with the final scores as priors
    print(final_score)
    if(np.sum(final_score)==0):
	    return np.random.choice(connects,replace=False, size = k)
    p = final_score - np.min(final_score) 
    p/=np.sum(p)
    print(p)
    if(np.sum(p!=0)<=k):
	    return np.random.choice(connects,replace=False, size = k)
    return np.random.choice(connects, size = k,replace = False, p = p)    

def add_edge_to_graph(follower,following):
	G=pickle.load(open('graph.txt','rb'))
	G.add_edge(follower,following)
	pickle.dump(G, open('graph.txt', 'wb'))
def add_node_to_graph(person_id):
	G=pickle.load(open('graph.txt','rb'))
	G.add_node(person_id)
	pickle.dump(G, open('graph.txt', 'wb'))


def recommend_follow(person_id):
	G=pickle.load(open('graph.txt','rb'))
	H = G.to_undirected()
	friends = {n for n in G.neighbors(person_id)}
	recommendation = recommendor(Gr = H,curr_user = person_id,k = 2, rad=1, friends=friends)
	return recommendation
def initialize_graph(request):
	G=nx.DiGraph()
	f=Following.objects.all()
	p=UserProfile.objects.all()
	for person in p:
		G.add_node(person.id)
	for rel in f:
		G.add_edge(rel.follower.id,rel.following.id)
	pickle.dump(G, open('graph.txt', 'wb'))

	return HttpResponse("Graph Initialized at graph.txt")


def remove_edge_graph(follower,following):
	G=pickle.load(open('graph.txt','rb'))
	G.remove_edge(follower,following)
	pickle.dump(G, open('graph.txt', 'wb'))

###### Views ######
@login_required
def feed(request):

	trends=Hashtag.objects.all()
	qaits = QAIT.objects.order_by('-date','-time')[:100]
	people=UserProfile.objects.filter(id__in=recommend_follow(UserProfile.objects.get(user=request.user).id))
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
		add_node_to_graph(p.id)
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
	parent_qait=QAIT.objects.get(id=qait_id)
	qaits = Reply.objects.filter(reply_to=q)
	people=UserProfile.objects.order_by('?')[:5]
	return render(request,"main/feed.html",context={
		'feed_title':'Replies for Qait',
		'trends':trends,
		'qaits': qaits,
		'people':people,
		'parent_qait':parent_qait,
	})
def create_following(request):

	following=UserProfile.objects.get(id=request.POST['person_id'])
	follower=UserProfile.objects.get(user=User.objects.get(username=request.user))
	f,created=Following.objects.get_or_create(follower=follower,following=following)
	if(not created):
		f.delete()

		remove_edge_graph(follower.id,following.id)
	else:
		f.save()

		add_edge_to_graph(follower.id,following.id)

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
def report_status(request,qait_id):
	return HttpResponse(flag_qait(QAIT.objects.get(id=qait_id).content))