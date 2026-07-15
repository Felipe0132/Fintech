from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('inicio/', views.inicio, name='inicio'),
    path('registrar-account', views.registrar_account, name="registrar_account"),
    path('registrar-transiction/', views.registrar_transiction, name='registrar_transiction'),
    path('registrar-category', views.registrar_category, name='registrar_category'),
    path('receitas-by-params', views.receitas_by_params, name="receitas_by_params"),
    path('gastos-by-params', views.gastos_by_params, name="gastos_by_params"),
    path('update-transiction', views.update_transiction, name="update_transiction"),
    path('delete-transiction', views.delete_transiction, name="delete_transiction"),
]