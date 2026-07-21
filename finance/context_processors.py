from .models import Account, Category

def global_finance_context(request):
    if request.user.is_authenticated:
        return {
            'global_accounts': Account.objects.filter(user=request.user),
            'global_categories_receita': Category.objects.filter(user=request.user, type="R"),
            'global_categories_gasto': Category.objects.filter(user=request.user, type="G"),
        }
    return {}
