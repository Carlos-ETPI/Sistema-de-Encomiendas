from django.forms import ModelForm
import re
from django import forms
from .models import Repartidor

class RepartidorForm(forms.ModelForm):
    id_repartidor = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'id'}))
    nombres = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}))
    apellidos = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}))
    DUI_persona = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DUI'}))
    telefono_repartidor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}))

    def clean_DUI_persona(self):
        dui = self.cleaned_data['DUI_persona']
        dui_regex = r'^\d{8}-\d{1}$'  # Expresión regular para DUI: ocho dígitos seguidos de guion y un dígito
        if not re.match(dui_regex, dui):
            raise forms.ValidationError("Formato de DUI inválido. Debe ser xxxxxxxx-x.")
        return dui
    
    def clean_telefono_repartidor(self):
        telefono = self.cleaned_data['telefono_repartidor']
        telefono_regex = r'^\d{4}-\d{4}$'  # Expresión regular para teléfono: cuatro dígitos seguidos de guion y otros cuatro dígitos
        if not re.match(telefono_regex, telefono):
            raise forms.ValidationError("Formato de teléfono inválido. Debe ser xxxx-xxxx.")
        return telefono

    class Meta:
        model = Repartidor
        fields = [ 'nombres', 'apellidos', 'DUI_persona', 'telefono_repartidor']

