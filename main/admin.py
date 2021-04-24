from django.contrib import admin

# Register your models here.
from .models import QAIT, Profile

admin.site.register(QAIT)
admin.site.register(Profile)
