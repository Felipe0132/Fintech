from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(ProfileUser, UserAdmin)
admin.site.register(Gasto)
admin.site.register(TipoGasto)
admin.site.register(Ganho)
admin.site.register(TipoGanho)