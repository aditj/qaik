from django.contrib import admin
from .models import Hashtag

admin.site.register(Hashtag)
# Register your models here.
from .models import QAIT, UserProfile

admin.site.register(QAIT)
admin.site.register(UserProfile)
