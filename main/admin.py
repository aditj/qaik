from django.contrib import admin
from .models import Hashtag,UserProfile,QAIT,Like

admin.site.register(Hashtag)
admin.site.register(UserProfile)

admin.site.register(QAIT)
admin.site.register(Like)