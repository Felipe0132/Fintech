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

    gastos = Gasto.objects.filter(user=user, is_paid=True)
    ganhos = Ganho.objects.filter(user=user)

    tipos_gastos = TipoGasto.objects.filter(user=user)
    tipos_ganhos = TipoGanho.objects.filter(user=user)

    total_gastos = sum_by_value(gastos)
    total_ganhos = sum_by_value(ganhos)

    saldo_atual = float(total_ganhos) - float(total_gastos)

    gastos_not_paid = Gasto.objects.filter(user=user, is_paid=False)

    saldo_imaginario = saldo_atual - float(sum_by_value(gastos_not_paid))

    grafico_gasto = grafico_by_category_gasto(gastos, user)
    grafico_ganho = grafico_by_category_ganho(ganhos, user)
    grafico_gasto_not_paid = grafico_by_category_gasto_not_paid(gastos_not_paid, user)

    user_context = {"gastos":gastos.order_by('-id')[:5], "ganhos":ganhos.order_by('-id')[:5], "total_gastos":total_gastos, "total_ganhos":total_ganhos, "saldo_atual":saldo_atual, "tipos_gastos":tipos_gastos, "tipos_ganhos":tipos_ganhos, 'gastos_not_paid':gastos_not_paid, "saldo_imaginario":saldo_imaginario, "grafico_gasto":grafico_gasto, "grafico_ganho":grafico_ganho, "grafico_gasto_not_paid":grafico_gasto_not_paid}

    return render(request, "finance/dashboard.html", context=user_context)

@login_required(login_url="/finance/login/")
def registrar_gasto(request):
    if request.method == "GET":
        return redirect('finance:dashboard')
    
    value = request.POST.get('value')
    description = request.POST.get('description')
    date_paid = request.POST.get('date_paid')
    is_paid = request.POST.get('is_paid') == 'True' # Recebe ou True ou Null do html

    type_id = request.POST.get('type') # Do html recebe so o id, ai o Django entende linkando so o type_id

    Gasto.objects.create(value=value, description=description, date_paid=date_paid, is_paid=is_paid, type_id=type_id if type_id else None, user=request.user)

    return redirect('finance:dashboard')

@login_required(login_url="/finance/login/")
def registrar_ganho(request):
    if request.method == "GET":
        return redirect('finance:dashboard')
    
    value = request.POST.get('value')
    description = request.POST.get('description')
    date_paid = request.POST.get('date_paid')
    is_paid = request.POST.get('is_paid') == 'True' # Recebe ou True ou Null do html

    type_id = request.POST.get('type') # Do html recebe so o id, ai o Django entende linkando so o type_id

    Ganho.objects.create(value=value, description=description, date_paid=date_paid, is_paid=is_paid, type_id=type_id if type_id else None, user=request.user)

    return redirect('finance:dashboard')

@login_required(login_url="/finance/login/")
def registrar_tipo_gasto(request):
    if request.method == "GET":
        return redirect('finance:dashboard')

    name = request.POST.get('name')

    if not(TipoGasto.objects.filter(name=name, user=request.user).exists()):     
        TipoGasto.objects.create(name=name, user=request.user)

    return redirect('finance:dashboard')

@login_required(login_url="/finance/login/")
def registrar_tipo_ganho(request):
    if request.method == "GET":
        return redirect('finance:dashboard')

    name = request.POST.get('name')

    if not(TipoGanho.objects.filter(name=name, user=request.user).exists()):     
        TipoGanho.objects.create(name=name, user=request.user)

    return redirect('finance:dashboard')