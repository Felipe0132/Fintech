from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('finance/')), # Caminho padrao inicial

    path('admin/', admin.site.urls),
    path('finance/', include('finance.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
