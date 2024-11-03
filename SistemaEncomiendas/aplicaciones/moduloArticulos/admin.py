from django.contrib import admin
from .models import ListadoMarcas
from .models import TipoArticulo
from .models import Servicio
from .models import ListadoImpuesto
from .models import Articulo_Auxiliar


# Register your models here.
admin.site.register(ListadoMarcas)
admin.site.register(TipoArticulo)
admin.site.register(Servicio)
admin.site.register(ListadoImpuesto)
admin.site.register(Articulo_Auxiliar)