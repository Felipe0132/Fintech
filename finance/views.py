from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
from .analytics import *
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


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
        return redirect('finance:inicio')        
    
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
def inicio(request):
    user = request.user

    accounts = Account.objects.filter(user=user)

    receitas = Transaction.objects.filter(user=user, type="R")
    gastos = Transaction.objects.filter(user=user, type="G", is_paid=True)

    categories_receita = Category.objects.filter(user=user, type="R")
    categories_gasto = Category.objects.filter(user=user, type="G")

    total_receitas = sum_by_value(receitas)
    total_gastos = sum_by_value(gastos)

    saldo_atual = total_receitas - total_gastos

    gastos_not_paid = Transaction.objects.filter(user=user, type="G", is_paid=False)

    saldo_imaginario = saldo_atual - sum_by_value(gastos_not_paid)

    user_context = {"gastos":gastos.order_by('-id')[:5],            
                    "receitas":receitas.order_by('-id')[:5], 
                    "total_gastos":total_gastos, 
                    "total_receitas":total_receitas, 
                    "saldo_atual":saldo_atual, 
                    "categories_receita":categories_receita, 
                    "categories_gasto":categories_gasto, 
                    "accounts":accounts, 
                    "gastos_not_paid":gastos_not_paid.order_by('-id')[:5], 
                    "saldo_imaginario":saldo_imaginario
                    }

    return render(request, "finance/inicio.html", context=user_context)

@login_required(login_url="/finance/login/")
def registrar_account(request):
    if request.method == "GET":
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('finance:inicio')
    
    name = request.POST.get('name')

    if not(Account.objects.filter(name=name, user=request.user).exists()):     
        Account.objects.create(name=name, user=request.user)

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('finance:inicio')

@login_required(login_url="/finance/login/")
def registrar_transiction(request):
    if request.method == "GET":
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('finance:inicio')
    
    type = request.POST.get('type')
    description = request.POST.get('description')
    value = request.POST.get('value')
    date = request.POST.get('date_paid')
    is_paid = request.POST.get('is_paid') == 'True' # Recebe ou True ou Null do html

    category_id = request.POST.get('category') # Do html recebe so o id, ai o Django entende linkando so o category_id

    account_id = request.POST.get('account')

    Transaction.objects.create(value=value, type=type, description=description, date=date, is_paid=is_paid, category_id=category_id if category_id else None, account_id=account_id, user=request.user)

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('finance:inicio')
    
@login_required(login_url="/finance/login/")
def registrar_category(request):
    if request.method == "GET":
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('finance:inicio')
    
    name = request.POST.get('name')
    type = request.POST.get('type')

    if not(Category.objects.filter(name=name, type=type, user=request.user).exists()):     
        Category.objects.create(name=name, type=type, user=request.user)

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('finance:inicio')

    
@login_required(login_url="/finance/login/")
def gastos_by_params(request):
    user = request.user
    gastos_consultados = Transaction.objects.filter(user=user, type="G")

    if request.method == "POST":
        description_search = request.POST.get('description_search')
        date_start = request.POST.get('date_start')
        date_end = request.POST.get('date_end')
        value = request.POST.get('value')
        category_id = request.POST.get('category')
        is_paid = request.POST.get('is_paid')
        account_id = request.POST.get('account')

        if description_search:
            gastos_consultados = gastos_consultados.filter(description__icontains=description_search)

        if date_start:
            gastos_consultados = gastos_consultados.filter(date__gte=date_start)

        if date_end:
            gastos_consultados = gastos_consultados.filter(date__lte=date_end)

        if value:
            gastos_consultados = gastos_consultados.filter(value=value)

        if category_id:
            gastos_consultados = gastos_consultados.filter(category_id=category_id)

        if is_paid == "True":
            gastos_consultados = gastos_consultados.filter(is_paid=True)

        if is_paid == "False":
            gastos_consultados = gastos_consultados.filter(is_paid=False)

        if account_id:
            gastos_consultados = gastos_consultados.filter(account_id=account_id)

    categories = Category.objects.filter(user=user, type="G")
    accounts = Account.objects.filter(user=user)

    receitas = Transaction.objects.filter(user=user, type="R")
    gastos = Transaction.objects.filter(user=user, type="G", is_paid=True)

    total_receitas = sum_by_value(receitas)
    total_gastos = sum_by_value(gastos)

    saldo_atual = total_receitas - total_gastos

    gastos_not_paid = Transaction.objects.filter(user=user, type="G", is_paid=False)

    total_gastos_not_paid = sum_by_value(gastos_not_paid)

    saldo_imaginario = saldo_atual - total_gastos_not_paid

    context = {"gastos_consultados":gastos_consultados.order_by('-date'), 
               "categories":categories, 
               "accounts":accounts,
               "total_gastos":total_gastos,
               "saldo_atual":saldo_atual,
               "total_gastos_not_paid":total_gastos_not_paid,
               "saldo_imaginario":saldo_imaginario
               }

    return render(request, 'finance/gastos.html', context=context)    

@login_required(login_url="/finance/login/")
def receitas_by_params(request):
    user = request.user
    receita_consultados = Transaction.objects.filter(user=user, type="R")

    if request.method == "POST":
        description_search = request.POST.get('description_search')
        date_start = request.POST.get('date_start')
        date_end = request.POST.get('date_end')
        value = request.POST.get('value')
        category_id = request.POST.get('category')
        account_id = request.POST.get('account')

        if description_search:
            receita_consultados = receita_consultados.filter(description__icontains=description_search)

        if date_start:
            receita_consultados = receita_consultados.filter(date__gte=date_start)

        if date_end:
            receita_consultados = receita_consultados.filter(date__lte=date_end)

        if value:
            receita_consultados = receita_consultados.filter(value=value)

        if category_id:
            receita_consultados = receita_consultados.filter(category_id=category_id)

        if account_id:
            receita_consultados = receita_consultados.filter(account_id=account_id)

    categories = Category.objects.filter(user=user, type="R")
    accounts = Account.objects.filter(user=user)

    receitas = Transaction.objects.filter(user=user, type="R")
    gastos = Transaction.objects.filter(user=user, type="G", is_paid=True)

    total_receitas = sum_by_value(receitas)
    total_gastos = sum_by_value(gastos)

    saldo_atual = total_receitas - total_gastos

    gastos_not_paid = Transaction.objects.filter(user=user, type="G", is_paid=False)

    total_gastos_not_paid = sum_by_value(gastos_not_paid)

    saldo_imaginario = saldo_atual - total_gastos_not_paid

    context = {"receita_consultados":receita_consultados.order_by('-date'), 
               "categories":categories, 
               "accounts":accounts,
               "total_receitas":total_receitas,
               "saldo_atual":saldo_atual,
               "saldo_imaginario":saldo_imaginario
               }

    return render(request, 'finance/receita.html', context=context)   
    
@login_required(login_url="/finance/login/")    
def update_transiction(request):
    if request.method == "GET":
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('finance:inicio')
    
    user = request.user
    type_id = request.POST.get('type')
    
    transaction_to_update = get_object_or_404(Transaction, id=request.POST.get('transaction_id'), type=type_id, user=user)

    description = request.POST.get('description')
    date = request.POST.get('date_paid')
    value = request.POST.get('value')
    category_id = request.POST.get('category')
    account_id = request.POST.get('account')

    if description:
        transaction_to_update.description = description
    if date:
        transaction_to_update.date = date
    if value:
        transaction_to_update.value = value
    transaction_to_update.is_paid = request.POST.get('is_paid') == 'True'
    if category_id:
        transaction_to_update.category_id = category_id
    if account_id:
        transaction_to_update.account_id = account_id

    transaction_to_update.save()

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('finance:inicio')

@login_required(login_url="/finance/login/")
def delete_transiction(request):
    if request.method == "GET":
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('finance:inicio')
    
    user = request.user

    transaction = get_object_or_404(Transaction, id=request.POST.get('transaction_id'), user=user)
    transaction.delete()

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('finance:inicio')

@login_required(login_url="/finance/login/")
def delete_account(request):
    if request.method == "GET":
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('finance:inicio')
    
    user = request.user

    account = get_object_or_404(Account, id=request.POST.get('account_id'), user=user)
    account.delete()

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('finance:inicio')

@login_required(login_url="/finance/login/")
def delete_category(request):
    if request.method == "GET":
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('finance:inicio')
    
    user = request.user

    category = get_object_or_404(Category, id=request.POST.get('category_id'), user=user)
    category.delete()

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('finance:inicio')

@login_required(login_url="/finance/login/")    
def update_account(request):
    if request.method == "GET":
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('finance:inicio')
    
    user = request.user
    
    account_to_update = get_object_or_404(Account, id=request.POST.get('account_id'), user=user)

    name = request.POST.get('name')

    if name:
        account_to_update.name = name

    account_to_update.save()

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('finance:inicio')

@login_required(login_url="/finance/login/")    
def update_category(request):
    if request.method == "GET":
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('finance:inicio')
    
    user = request.user
    
    category_to_update = get_object_or_404(Category, id=request.POST.get('category_id'), user=user)

    name = request.POST.get('name')

    if name:
        category_to_update.name = name

    category_to_update.save()

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('finance:inicio')


@login_required(login_url="/finance/login")
def accounts_categories(request):

    user = request.user

    accounts = Account.objects.filter(user=user)

    categories = Category.objects.filter(user=user)

    categories_receita = categories.filter(type="R")
    categories_gasto = categories.filter( type="G")

    user_context = {"categories":categories,
                    "categories_receita":categories_receita, 
                    "categories_gasto":categories_gasto, 
                    "accounts":accounts,
                    }

    return render(request, 'finance/accounts_categories.html', user_context)

@login_required(login_url="/finance/login")
def dashboard_mensal(request):
    today = date.today()
    user = request.user

    if request.method == "POST":
        selected_month = request.POST.get("selected_month")
        compare_month = request.POST.get("compare_month")
    else:
        selected_month = today.strftime("%Y-%m")
        compare_month = (today - relativedelta(months=1)).strftime("%Y-%m")

    selected_ref = datetime.strptime(selected_month, "%Y-%m")
    compare_ref = datetime.strptime(compare_month, "%Y-%m")
        
    receitas_selected = Transaction.objects.filter(user=user, type="R", date__year=selected_ref.year, date__month=selected_ref.month)
    gastos_selected = Transaction.objects.filter(user=user, type="G", date__year=selected_ref.year, date__month=selected_ref.month)

    
    receitas_compare = Transaction.objects.filter(user=user, type="R", date__year=compare_ref.year, date__month=compare_ref.month)
    gastos_compare = Transaction.objects.filter(user=user, type="G", date__year=compare_ref.year, date__month=compare_ref.month)
    
    accounts = Account.objects.filter(user=user)
    categories_receita = Category.objects.filter(user=user, type="R")
    categories_gastos = Category.objects.filter(user=user, type="G")

    value_by_category_receita_selected = sum_by_category(receitas_selected)
    value_by_category_gastos_selected = sum_by_category(gastos_selected)

    user_context = {"selected_month":selected_month,
                    "compare_month":compare_month,
                    "receitas_selected":receitas_selected,
                    "gastos_selected": gastos_selected,
                    "receitas_compare":receitas_compare,
                    "gastos_compare":gastos_compare,
                    "accounts":accounts,
                    "categories_receita":categories_receita,
                    "categories_gastos":categories_gastos,
                    "value_by_category_receita_selected":value_by_category_receita_selected,
                    "value_by_category_gastos_selected":value_by_category_gastos_selected
                    }

    return render(request, 'finance/dashboard_mensal.html', user_context)
