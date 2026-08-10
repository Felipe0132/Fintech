from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'finance'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='finance/password_reset_confirm.html', success_url=reverse_lazy('finance:password_reset_complete')), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='finance/password_reset_complete.html'), name='password_reset_complete'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('validar-cadastro/', views.validar_cadastro, name='validar_cadastro'),
    path('inicio/', views.inicio, name='inicio'),
    path('registrar-account', views.registrar_account, name="registrar_account"),
    path('registrar-transiction/', views.registrar_transiction, name='registrar_transiction'),
    path('registrar-category', views.registrar_category, name='registrar_category'),
    path('receitas-by-params', views.receitas_by_params, name="receitas_by_params"),
    path('gastos-by-params', views.gastos_by_params, name="gastos_by_params"),
    path('update-transiction', views.update_transiction, name="update_transiction"),
    path('delete-transiction', views.delete_transiction, name="delete_transiction"),
    path('accounts-categories/', views.accounts_categories, name="accounts_categories"),
    path('delete-account/', views.delete_account, name="delete_account"),
    path('delete-category/', views.delete_category, name="delete_category"),
    path('update-account', views.update_account, name="update_account"),
    path('update-category', views.update_category, name="update_category"),
    path('dashboard-mensal', views.dashboard_mensal, name="dashboard_mensal")
]