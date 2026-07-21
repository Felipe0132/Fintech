from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(ProfileUser, UserAdmin)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Account)