from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
from dateutil.relativedelta import relativedelta
import uuid

class ProfileUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' # Django assim entende que o email sera o diferencial
    REQUIRED_FIELDS = ['username'] # Aqui ainda mantem o username importante, mas nao como campo de login

class Account(models.Model):
    name = models.CharField(max_length=255)
    value = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # safer, since the login is based on a custom field (email)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    class Type(models.TextChoices):
        GASTO = "G", "Gasto"
        RECEITA = "R", "Receita"

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=Type.choices) # Recive 1 char and return the choice, G -> Gasto

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # safer, since the login is based on a custom field (email)

    def __str__(self):
        return self.name
    
class Transaction_installment(models.Model):
    description = models.CharField(max_length=255)
    total_value = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    installments_count = models.PositiveSmallIntegerField()
    first_date = models.DateField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property # Used because it behaves like a computed attribute — no parentheses needed to get the value
    def installment_value(self):
        return round(int(self.total_value) / self.installments_count, 2)
    
    @property
    def remaining_installments(self):
        return self.transactions.filter(is_paid=False).count()

    def __str__(self):
        return f"{self.description} ({self.installments_count}x)"

    def generate_installments(self):
        transactions = [
            Transaction(
                description=f"{self.description}",
                value = self.installment_value,
                type=Transaction.Type.GASTO,
                date=self.first_date + relativedelta(months=i),
                is_paid=False,
                category=self.category,
                account=self.account,
                user=self.user,
                transaction_installment=self,
                installment_number=i+1,
            )
            for i in range(self.installments_count) # list comprehension — equivalent to a for-loop appending to a list
        ]
        return Transaction.objects.bulk_create(transactions) # creates all records in a single query, instead of calling save() individually for each

class Transaction(models.Model):
    class Type(models.TextChoices):
        GASTO = "G", "Gasto"
        RECEITA = "R", "Receita"

    description = models.CharField(max_length=255)
    value = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    type = models.CharField(max_length=1, choices=Type.choices)
    date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    transaction_installment = models.ForeignKey("Transaction_installment", null=True, blank=True, on_delete=models.CASCADE, related_name="transactions")
    # Every transaction linked to an installment plan will reference it here;
    # for a single (non-installment) transaction, this stays None — filter using isnull=True/False
    installment_number = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.description