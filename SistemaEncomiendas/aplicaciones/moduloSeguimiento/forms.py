from django.forms import ModelForm
from django import forms
from ..moduloOrdPaq.models import Pedido, Viaje, Cliente, Ruta, Recordatorio, CustomUser

import re
from django.core.exceptions import ValidationError

#Formulario para crear pedido
class estadosForm(forms.ModelForm):
    # Campo adicional que no se guarda en la base de datos
    mensaje = forms.CharField(
        required=False,  # Opcional
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Escribe el mensaje aquí...'
        }),
        label="Detalles de estado"
    )

    class Meta:
        model = Pedido
        fields = ['estado_pedido'] 