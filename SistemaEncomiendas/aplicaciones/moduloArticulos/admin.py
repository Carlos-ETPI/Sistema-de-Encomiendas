from django.contrib import admin
from .models import ListadoMarcas
from .models import TipoArticulo
from .models import Servicio
from .models import ListadoImpuesto


# Register your models here.
admin.site.register(ListadoMarcas)
admin.site.register(TipoArticulo)
admin.site.register(Servicio)
admin.site.register(ListadoImpuesto)