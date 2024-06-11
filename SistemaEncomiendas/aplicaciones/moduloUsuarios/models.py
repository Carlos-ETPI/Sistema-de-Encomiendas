from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    idUsuario=models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=60, blank=True, null=False)
    apellidos = models.CharField(max_length=60, blank=True, null=False)
    dui = models.CharField(max_length=10, blank=True, null=False, unique=True)
    activo = models.BooleanField(default=True)
