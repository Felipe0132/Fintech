from django.db import models
from django.contrib.auth.models import AbstractUser

class ProfileUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' # Django assim entende que o email sera o diferencial
    REQUIRED_FIELDS = ['username'] # Aqui ainda mantem o username importante, mas nao como campo de login