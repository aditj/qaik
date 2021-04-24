from django.urls import path

from . import views

urlpatterns = [
path('feed',views.feed),
path('login',views.login_view),
path('register',views.register),
path('logout',views.logout_view),
path('create_qait',views.create_qait),
<<<<<<< HEAD
path('profile',views.profile)
=======
path('like_dislike', views.like_dislike),
>>>>>>> d45dfe58a9fff634e122b3f85583b2c0e8a6498b
]