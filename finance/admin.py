from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ProfileUser

admin.site.register(ProfileUser, UserAdmin)