from django.urls import path

from . import views

urlpatterns = [
path('feed',views.feed),
path('login',views.login_view),
path('register',views.register),
path('logout',views.logout_view),
path('create_qait',views.create_qait)
]