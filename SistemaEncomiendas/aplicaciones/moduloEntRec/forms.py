from django import forms
from ..moduloUsuarios.models import Repartidor  
from ..moduloEntRec.models import Ruta  


class RutaForm(forms.ModelForm):
    repartidor = forms.ModelChoiceField(
    queryset=None,
    widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': 'Repartidor', 'required': 'required'}
    )
)

    fecha = forms.DateField(
        widget= forms.DateInput(
            attrs={'class': 'form-control', 'placeholder': 'Fecha'}
        )
    )
    nombre_ruta = forms.CharField(
        widget= forms.TextInput(
            attrs ={'class': 'form-control', 'placeholder': 'Nombre Ruta'}
        )
    )
    zona = forms.CharField(
        widget= forms.TextInput(
            attrs ={'class': 'form-control', 'placeholder': 'Zona'}
        )
    )
    class Meta:
        model = Ruta
        fields = ['repartidor', 'fecha','nombre_ruta','zona']
    
    
def clean_id_repartidor(self):
    id_repartidor = self.cleaned_data.get('id_repartidor')
    if id_repartidor is None:
        raise forms.ValidationError("Debe seleccionar un repartidor.")
    return id_repartidor
