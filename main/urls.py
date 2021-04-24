from django.urls import path

from . import views

urlpatterns = [
path('feed',views.feed),
path('login',views.login_view),
path('register',views.register),
path('logout',views.logout_view),
path('create_qait',views.create_qait),
path('profile/<str:user>',views.profile),
path('like_dislike', views.like_dislike),
path('reply',views.reply),
path('replies/<int:qait_id>',views.see_replies),
path('follow',views.create_following),
path('search/<str:query>',views.search),

]
