from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings

class ProfileUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' # Django assim entende que o email sera o diferencial
    REQUIRED_FIELDS = ['username'] # Aqui ainda mantem o username importante, mas nao como campo de login

class TipoGasto(models.Model):
    name = models.CharField(max_length=255)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Gasto(models.Model):
    value = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date_paid = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=True)

    type = models.ForeignKey(TipoGasto, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # safer, since the login is based on a custom field (email)

    def __str__(self):
        return self.description

class TipoGanho(models.Model):
    name = models.CharField(max_length=255)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    

class Ganho(models.Model):
    value = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date_paid = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=True)

    type = models.ForeignKey(TipoGanho, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # safer, since the login is based on a custom field (email)

    def __str__(self):
        return self.description