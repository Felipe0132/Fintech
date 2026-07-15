from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('inicio/', views.inicio, name='inicio'),
    path('registrar-transiction/', views.registrar_transiction, name='registrar_transiction'),
    path('registrar-category', views.registrar_category, name='registrar_category'),
    path('consultar-transictions-by-params', views.consultar_transictions_by_params, name="consultar_type_by_params"),
    path('atualizar-transictions', views.atualizar_transictions, name="atualizar_transictions"),
    path('delete-transictions', views.delete_transictions, name="delete_transictions"),
]