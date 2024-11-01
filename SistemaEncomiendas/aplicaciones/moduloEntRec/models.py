from django.db import models
from ..moduloUsuarios.models import Repartidor
# Create your models here.
class PuntoEntregaRecepcion(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    coordenadas = models.CharField(max_length=100, null=True, blank=True)
    
class Ruta(models.Model):
    id_ruta = models.AutoField(primary_key=True)
    id_repartidor = models.ForeignKey(Repartidor, on_delete=models.RESTRICT)
    fecha = models.DateField()
    nombre_ruta = models.CharField(max_length=50)
    zona = models.CharField(max_length=50)