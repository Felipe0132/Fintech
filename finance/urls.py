from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registrar-gasto/', views.registrar_gasto, name='registrar_gasto'),
]