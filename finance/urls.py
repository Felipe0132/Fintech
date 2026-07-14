from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registrar-gasto/', views.registrar_gasto, name='registrar_gasto'),
    path('registrar-ganho/', views.registrar_ganho, name='registrar_ganho'),
    path('registrar-tipo-gasto', views.registrar_tipo_gasto, name='registrar_tipo_gasto'),
    path('registrar-tipo-ganho', views.registrar_tipo_ganho, name='registrar_tipo_ganho'),
    path('consultar-gastos-by-params', views.consultar_gastos_by_params, name="consultar_gastos_by_params"),
    path('consultar-ganhos-by-params', views.consultar_ganhos_by_params, name="consultar_ganhos_by_params"),
    path('atualizar-gasto', views.atualizar_gasto, name="atualizar_gasto"),
    path('atualizar-ganho', views.atualizar_ganho, name="atualizar_ganho"),
]