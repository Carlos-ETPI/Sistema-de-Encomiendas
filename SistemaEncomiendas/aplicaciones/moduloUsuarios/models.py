
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class CustomUser(AbstractUser):
    idUsuario=models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=50, blank=True, null=False)
    apellidos = models.CharField(max_length=50, blank=True, null=False)
    dui = models.CharField(max_length=10, blank=True, null=True, unique=True)
    activo = models.BooleanField(default=True)
    telefono =  models.CharField(max_length=10, blank=True, null=False)

class Cliente(models.Model):
    id_cliente=models.BigAutoField(primary_key=True)
    nombre_cliente=models.CharField(max_length=50,blank=True, null=False)
    apellido_cliente=models.CharField(max_length=50,blank=True, null=False)
    dui_cliente=models.CharField(max_length=10,blank=True, null=False)
    nacionalidad_cliente=models.CharField(max_length=50,blank=True, null=False)
    telefono_cliente=models.CharField(max_length=10,blank=True, null=False)
    email_cliente=models.CharField(max_length=50,blank=True, null=False)
    estado = models.BooleanField('estado', default=True)
    
class Repartidor(models.Model):
    id_repartidor = models.AutoField(primary_key=True)
    nombres=models.CharField(max_length=50)
    apellidos=models.CharField(max_length=50)
    DUI_persona=models.CharField(max_length=10,unique=True)
    telefono_repartidor=models.CharField(max_length=10, blank=True, null=False)
    def __str__(self):
            return f"{self.nombres} {self.apellidos}"    

class Telefono(models.Model):
    id_telefono = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    codigo_pais = models.CharField(max_length=3)
    numero = models.CharField(max_length=10)
