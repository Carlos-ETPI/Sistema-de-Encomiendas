from django.db import models

# Create your models here.
class Recordatorio(models.Model):
    id_recordatorio = models.AutoField(primary_key=True)
    fecha_entrega = models.DateField()
    num_peticiones = models.IntegerField()
