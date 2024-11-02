from django import forms
from .models import Articulo

class CrearArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['id_servicio', 'id_ti_articulo', 'id_lis_marcas', 'nombre_articulo', 'peso','cantidad','estado','impuestos_envio','costo_encomienda','costo_total_envio']
        
