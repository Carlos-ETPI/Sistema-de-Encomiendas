from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario',max_length=50, required=True,widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'autocomplete': 'off'}))
    password = forms.CharField(label='Clave', max_length=100, required=True,widget=forms.PasswordInput)
    
    

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña Actual'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nueva Contraseña'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar Nueva Contraseña'})