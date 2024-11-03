from django.forms import ModelForm
from django import forms
from .models import Pedido, Viaje, Cliente, Ruta, Recordatorio
from ..moduloUsuarios.models import CustomUser
from django.core.exceptions import ValidationError

#Formulario para crear pedido
class pedidoForm(forms.ModelForm):
    #Seleccion de llaves foraneas
    id_usuario = forms.ModelChoiceField(
        queryset= CustomUser.objects.all(),
        widget=forms.Select(attrs={
            'class':'form-control',
        })
    )
    id_viaje = forms.ModelChoiceField(
        queryset=Viaje.objects.all(),
        widget=forms.Select(attrs={
            'class':'form-control',
        }),
        required=False
    )
    id_cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(attrs={
            'class':'form-control',
        }),
        required=False
    )
    id_ruta = forms.ModelChoiceField(
        queryset=Ruta.objects.all(),
        widget=forms.Select(attrs={
            'class':'form-control',
        }),
        required=False
    )
    id_ubicacion = forms.ModelChoiceField(
        queryset=Recordatorio.objects.all(),
        widget=forms.Select(attrs={
            'class':'form-control',
        }),
        required=False
    )

    #Atributos propios de pedido
    punto_entrega = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Punto de entrega',
            'maxlength':'100',
            'autocomplete':'off'})
    )
    punto_recepcion = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Punto de recepcion',
            'maxlength':'100',
            'autocomplete':'off'})
    )
    region = forms.Select(
        attrs={
            'class':'form-control',
        }
    )
    estado_pedido = forms.Select(
        attrs={
            'class':'form-control',
        }
    )
    recogido = forms.CheckboxInput(
        attrs={
            'class':'form-check-input',
        }
    )
    total_peso_pe = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class':'form-control',
            'placeholder':'Total peso',
            'step':'0.01',
        })
    )

    class Meta:
        model = Pedido
        fields = ['id_usuario','id_viaje', 'id_cliente', 'id_ruta', 'id_ubicacion','punto_entrega','punto_recepcion','region','estado_pedido','recogido','total_peso_pe']

    #validaciones y acciones automaticas del formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        if not self.instance.pk:
            if 'numero_orden' in self.fields:
                self.fields['numero_orden'].widget.attrs['readonly'] = True

#formulario de actulizacion
class actualizarPedidoForm(forms.ModelForm):
    #Seleccion de llaves foraneas
    id_usuario = forms.ModelChoiceField(
        queryset= CustomUser.objects.all(),
        widget=forms.Select(attrs={
            'class':'form-control',
        })
    )
    id_viaje = forms.ModelChoiceField(
        queryset=Viaje.objects.all(),
        widget=forms.Select(attrs={
            'class':'form-control',
        }),
        required=False
    )
    id_cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(attrs={
            'class':'form-control',
        }),
        required=False
    )
    id_ruta = forms.ModelChoiceField(
        queryset=Ruta.objects.all(),
        widget=forms.Select(attrs={
            'class':'form-control',
        }),
        required=False
    )
    id_ubicacion = forms.ModelChoiceField(
        queryset=Recordatorio.objects.all(),
        widget=forms.Select(attrs={
            'class':'form-control',
        }),
        required=False
    )

    #Atributos propios de pedido
    punto_entrega = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Punto de entrega',
            'maxlength':'100',
            'autocomplete':'off'})
    )
    punto_recepcion = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Punto de recepcion',
            'maxlength':'100',
            'autocomplete':'off'})
    )
    region = forms.Select(
        attrs={
            'class':'form-control',
        }
    )
    estado_pedido = forms.Select(
        attrs={
            'class':'form-control',
        }
    )
    recogido = forms.CheckboxInput(
        attrs={
            'class':'form-check-input',
        }
    )
    total_peso_pe = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class':'form-control',
            'placeholder':'Total peso',
            'step':'0.01',
        })
    )

    class Meta:
        model = Pedido
        fields = ['id_usuario','id_viaje', 'id_cliente', 'id_ruta', 'id_ubicacion','punto_entrega','punto_recepcion','region','estado_pedido','recogido','total_peso_pe']

