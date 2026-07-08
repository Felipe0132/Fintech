from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


ProfileUser = get_user_model() # Substituir o User

def index(request):
    return render(request, 'finance/index.html')

def login(request):
    if request.method == "GET":
        return render(request, 'finance/login.html')
    
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(email=email, password=password)

    if user:
        login_django(request, user) # Navegador logado

        return render(request, "finance/dashboard")
    
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