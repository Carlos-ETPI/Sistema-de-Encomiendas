from django.db import models
from ..moduloUsuarios.models import Cliente, CustomUser
from ..moduloViajes. models import Viaje
from ..moduloSeguimiento.models import Ruta,Recordatorio
from ..moduloArticulos.models import Articulo
from django.dispatch import receiver
from django.db.models.signals import pre_save


# Create your models here.
class Paquete(models.Model):
    id_paquete = models.AutoField(primary_key=True)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.RESTRICT)
    destinatario = models.CharField(max_length=50)
    total_peso_pa = models.DecimalField(max_digits=10, decimal_places=2)
    
class Pedido(models.Model):
    #Definicion de opciones 
    REGION_CHOICES = [
        ('ES-US','El Salvador a Estados Unidos'),
        ('US-ES','Estados Unidos a El Salvador')
    ]

    ESTADO_CHOICES = [
        ('Enviado','Enviado'),
        ('Cancelado','Cancelado'),
        ('Preparado','Preparado')
    ]

    #Relaciones con modelos - no se incluye paquete ya que un pedido puede tener muchos paquetes pero un paquete solo puede tener un pedido, la relacion ira en el modelo paquete
    id_pedido = models.AutoField(primary_key=True)
    #Siempre se asiganara el usuario logeado a la creacion de pedido 
    id_usuario = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    id_viaje = models.ForeignKey(Viaje, on_delete=models.RESTRICT, null=True, blank=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT, null=True, blank=True)
    id_ruta = models.ForeignKey(Ruta, on_delete=models.RESTRICT, null=True, blank=True)
    id_ubicacion = models.ForeignKey(Recordatorio, on_delete=models.RESTRICT, null=True, blank=True)

    #atributos especificos del pedido
    numero_orden = models.CharField(max_length=20, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)#insertar automaticamente fecha de cracion
    fecha_modificacion = models.DateTimeField(auto_now=True)#insertar automaticamente ultima fecha de modificacion
    punto_entrega = models.CharField(max_length=100)
    punto_recepcion = models.CharField(max_length=100)
    region = models.CharField(max_length=5, choices=REGION_CHOICES)
    estado_pedido = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    recogido = models.BooleanField(default=False)#definir recogido como falso por defecto
    total_peso_pe = models.DecimalField(max_digits=10, decimal_places=2)

#creacion de numero de orden personalizada
@receiver(pre_save, sender = Pedido)
def set_numero_orden(sender, instance, **kwargs):
    if not instance.numero_orden:
        last_pedido = Pedido.objects.order_by('-id_pedido').first()
        if last_pedido:
            last_number = int(last_pedido.numero_orden.replace('#Ord',''))
            new_number = last_number + 1#incrementa en uno el numero de orden en base a la ultima orden registrada
        else:
            new_number = 1#no orden previa pone el numero en 1
        instance.numero_orden = f'#Ord{new_number}'