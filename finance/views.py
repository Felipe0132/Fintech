from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
from .analytics import *


ProfileUser = get_user_model() # Substituir o User

def index(request):
    return render(request, 'finance/index.html')

def login(request):
    if request.method == "GET":
        return render(request, 'finance/login.html')
    
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(username=email, password=password)

    if user:
        login_django(request, user) # Navegador logado
        return redirect('finance:dashboard')        
    
    return HttpResponse("Dados incorretos")

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'finance/cadastro.html')
    
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    if ProfileUser.objects.filter(email=email).exists():
        return HttpResponse("Ja existe um usuario com este Email!")
    
    ProfileUser.objects.create_user(username=username, email=email, password=password)

    return redirect('finance:login')

@login_required(login_url="/finance/login/")
def dashboard(request):
    user = request.user

    gastos = Gasto.objects.filter(user=user)
    ganhos = Ganho.objects.filter(user=user)
    total_gastos = sum_by_value(gastos)
    total_ganhos = sum_by_value(ganhos)
    saldo_atual = (float)(total_ganhos)-(float)(total_gastos)

    user_context = {"gastos":gastos.order_by('-id')[:5], "ganhos":ganhos.order_by('-id')[:5], "total_gastos":total_gastos, "total_ganho":total_ganhos, "saldo_atual":saldo_atual}

    return render(request, "finance/dashboard.html", context=user_context)