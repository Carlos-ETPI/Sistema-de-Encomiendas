from django.db import models
from django.core.validators import MinValueValidator

class Articulo(models.Model):
    
    TIPO_ESTADO_CHOICES = [
        ('Sin Estado', 'Prestigio'),
        ('Con Encomendistas', 'Lujo'),
        ('En Aduana', 'Lujo'),
        ('Enviado', 'Lujo'),
        ('Entregado', 'Lujo'),
    ]
    
    id_articulo = models.AutoField(primary_key=True)
    id_servicio = models.ForeignKey('Servicio', on_delete=models.RESTRICT)
    id_ti_articulo = models.ForeignKey('TipoArticulo', on_delete=models.RESTRICT, blank=True, null=True)
    id_lis_marcas = models.ForeignKey('ListadoMarcas', on_delete=models.RESTRICT, blank=True, null=True)
    nombre_articulo = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    estado = models.CharField(max_length=30,choices=TIPO_ESTADO_CHOICES,default='Sin Estado')
    impuestos_envio=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    costo_encomienda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_total_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Articulo_Auxiliar(models.Model):
    
    TIPO_ESTADO_CHOICES = [
        ('Sin Estado', 'Prestigio'),
        ('Con Encomendistas', 'Lujo'),
        ('En Aduana', 'Lujo'),
        ('Enviado', 'Lujo'),
        ('Entregado', 'Lujo'),
    ]
    
    id_articulo = models.AutoField(primary_key=True)
    id_servicio = models.ForeignKey('Servicio', on_delete=models.RESTRICT)
    id_ti_articulo = models.ForeignKey('TipoArticulo', on_delete=models.RESTRICT, blank=True, null=True)
    id_lis_marcas = models.ForeignKey('ListadoMarcas', on_delete=models.RESTRICT, blank=True, null=True)
    nombre_articulo = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    estado = models.CharField(max_length=30,choices=TIPO_ESTADO_CHOICES,default='Sin Estado')
    impuestos_envio=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    costo_encomienda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_total_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class TipoArticulo(models.Model):
    CATEGORIA_CHOICES=[
        ('PRENDAS DE VESTIR Y ACCESORIOS PARA HOMBRE', 'PRENDAS DE VESTIR Y ACCESORIOS PARA HOMBRE'),
        ('PRENDAS DE VESTIR Y ACCESORIOS PARA DAMA', 'PRENDAS DE VESTIR Y ACCESORIOS PARA DAMA'),
        ('PRENDAS DE VESTIR Y ACCESORIOS PARA NIÑOS Y BEBÉS', 'PRENDAS DE VESTIR Y ACCESORIOS PARA NIÑOS Y BEBÉS'),
        ('JUGUETES', 'JUGUETES'),
        ('UTILES ESCOLARES Y ARTICULOS DE OFICINA', 'UTILES ESCOLARES Y ARTICULOS DE OFICINA'),
        ('COSMÉTICOS, ACCESORIOS DE BELLEZA Y ARTICULOS DE HIGIENE PERSONAL', 'COSMÉTICOS, ACCESORIOS DE BELLEZA Y ARTICULOS DE HIGIENE PERSONAL'),
        ('APARATOS ELÉCTRICOS DEL HOGAR', 'APARATOS ELÉCTRICOS DEL HOGAR'),
        ('ALIMENTOS EMPACADOS O ENVASADOS', 'ALIMENTOS EMPACADOS O ENVASADOS'),
        ('HERRAMIENTAS', 'HERRAMIENTAS'),
        ('ARTICULOS NAVIDEÑOS', 'ARTICULOS NAVIDEÑOS'),
        ('OTROS ARTICULOS IMPORTADOS', 'OTROS ARTICULOS IMPORTADOS'),
    ]
    
    UNIDAD_MEDIDA_CHOICES = [
        ('Par', 'Par'),
        ('Unidad', 'Unidad'),
        ('Set', 'Set'),
        ('Conjunto', 'Conjunto'),
        ('Kilogramo', 'Kilogramo'),
        ('Docena', 'Docena'),
        ('Paquete', 'Paquete'),
        ('Juego', 'Juego'),
        ('Caja', 'Caja'),
        ('Bote', 'Bote'),
        ('Bolsa/Caja', 'Bolsa/Caja'),
        ('Botella', 'Botella'),
        ('Bolsa', 'Bolsa'),
        ('Libra', 'Libra'),
        ('Lata', 'Lata'),
        ('Caja', 'Caja'),
        ('Frasco', 'Frasco'),
        ('Equipo', 'Equipo'),
        ('Metro', 'Metro'),
        ('Yarda', 'Yarda'),
        ('Ramo', 'Ramo'),
        ('Kit', 'Kit'),
        ('Gramo', 'Gramo'),
        ('Pliego', 'Pliego'),
    ]

    TIPO_MARCA_CHOICES = [
        ('Prestigio', 'Prestigio'),
        ('Lujo', 'Lujo'),
        ('Otras Marcas', 'Otras Marcas'),
    ]

    id_ti_articulo = models.AutoField(primary_key=True)
    categoria_tipo=models.CharField(max_length=100,choices=CATEGORIA_CHOICES)
    nombre_tipo = models.CharField(max_length=50)
    tipo_marca = models.CharField(max_length=50,choices=TIPO_MARCA_CHOICES,default="Otras Marcas")
    unidad_medida = models.CharField(max_length=10,choices=UNIDAD_MEDIDA_CHOICES)
    cip = models.DecimalField(max_digits=10, decimal_places=2,default=0)

class Servicio(models.Model):
    NOMBRE_SERVICIOS_CHOICES = [
        ('Envio de Documentos', 'Envio de Documentos'),
        ('Envio de Medicamentos', 'Envio de Medicamentos'),
        ('Envio de Articulos Varios', 'Envio de Articulos Varios'),
        ('Correo de Comida', 'Correo de Comida'),
        ('Compras en linea', 'Compras en linea'),
    ]
    id_servicio = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=50,choices=NOMBRE_SERVICIOS_CHOICES)
    estandar=models.BooleanField(blank=True, default=False)
    personalizado=models.BooleanField(blank=True, default=False)
    shein=models.BooleanField(blank=True, default=False)
    precio_libra = models.DecimalField(max_digits=10, decimal_places=2,default=0)



class Cancelacion(models.Model):
    id_cancelacion = models.AutoField(primary_key=True)
    id_articulo = models.ForeignKey('Articulo', on_delete=models.RESTRICT, default="")
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    precio_envio = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=200)
    tipo_cancelacion = models.CharField(max_length=30)



class ListadoImpuesto(models.Model):
    
    id_lis_impuesto = models.AutoField(primary_key=True)
    id_ti_articulo = models.ForeignKey('TipoArticulo', on_delete=models.RESTRICT)  
    cip = models.DecimalField(max_digits=10, decimal_places=2)


#Modulo de la lista de marcas de lujo y prestigio
class ListadoMarcas(models.Model):
    TIPO_MARCA_CHOICES = [
        ('Prestigio', 'Prestigio'),
        ('Lujo', 'Lujo'),
    ]
    id_lis_marcas = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=50)
    tipo_marca = models.CharField(max_length=50,choices=TIPO_MARCA_CHOICES)
