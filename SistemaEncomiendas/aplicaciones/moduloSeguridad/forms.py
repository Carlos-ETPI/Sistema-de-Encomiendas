from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'autocomplete': 'on'}),
        error_messages={
            'required': 'Por favor ingrese su nombre de usuario.',
            'max_length': 'El nombre de usuario no puede exceder los 50 caracteres.'
        }
    )
    password = forms.CharField(
        label='Contraseña',
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
        error_messages={
            'required': 'Por favor ingrese su contraseña.',
            'max_length': 'La contraseña no puede exceder los 100 caracteres.'
        }
    )
    
    
    

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña Actual'},
        error_messages={
            'required': 'Por favor ingrese su contraseña Actual.',
            'max_length': 'La contraseña no puede exceder los 100 caracteres.'
        })
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nueva Contraseña'},
        error_messages={
            'required': 'Por favor ingrese su nueva contraseña.',
            'max_length': 'La contraseña no puede exceder los 100 caracteres.'
        })
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar Nueva Contraseña'},
        error_messages={
            'required': 'Por favor ingrese su nueva contraseña(Confirmacion).',
            'max_length': 'La contraseña no puede exceder los 100 caracteres.'
        })