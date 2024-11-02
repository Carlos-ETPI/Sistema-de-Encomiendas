from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Modulo de viaje.
class Viaje(models.Model):
    id_viaje = models.AutoField(primary_key=True)
    fecha_ida = models.DateField()
    fecha_vuelta = models.DateField()
    destino=models.CharField(max_length=100)
    cantidad_personas = models.IntegerField(validators=[
            MaxValueValidator(99),
            MinValueValidator(1)  
        ])
    precio_boleto_ida=models.DecimalField(max_digits=10, decimal_places=2)
    precio_boleto_retorno=models.DecimalField(max_digits=10, decimal_places=2)

