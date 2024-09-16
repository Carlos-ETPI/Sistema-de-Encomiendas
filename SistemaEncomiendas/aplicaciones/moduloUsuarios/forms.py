from django.forms import ModelForm
from django import forms
from .models import Repartidor,Cliente, CustomUser

import re
from django.core.exceptions import ValidationError
from .validators import validar_dui,validar_telefono, validar_password



class RepartidorForm(forms.ModelForm):
    nombres = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}))
    apellidos = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}))
    DUI_persona = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DUI','id':'DUI','maxlength':'10'}),validators=[validar_dui])
    telefono_repartidor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono','id':'tel','maxlength':'9'}),validators=[validar_telefono])
    class Meta:
        model = Repartidor
        fields = [ 'nombres', 'apellidos', 'DUI_persona', 'telefono_repartidor']

#formulario para crear empleados
class empleadoForm(forms.ModelForm):
    nombres = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'nombres',
            'maxlength':'50',
            'autocomplete':'off'})
        )
    apellidos = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Apellidos',
            'maxlength':'50',
            'autocomplete':'off'})
        )
    dui = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'DUI',
            'id':'DUI',
            'maxlength':'10',
            'autocomplete':'off'}),validators=[validar_dui]
        )
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Telefono',
            'maxlength':'9',
            'autocomplete':'off'}),validators=[validar_telefono]
        )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Nombre de usuario',
            'autocomplete':'off'})
        )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder':'youremail@extension.com',
            'autocomplete':'off'})
        )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Contraseña',
            'autocomplete':'off'})
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Contraseña',
            'autocomplete':'off'
        })
    )
    class Meta:
        model = CustomUser
        fields = ['nombres', 'apellidos', 'dui','telefono', 'username', 'email', 'password']
    
    #email unico
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('La direccion de correo electronico ya esta en uso.')
        return email
    
    #username unico
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('El nombre de usuario no esta disponible.')
        return username

    #dui unico
    def clean_dui(self):
        dui = self.cleaned_data.get('dui')
        if CustomUser.objects.filter(dui=dui).exists():
            raise ValidationError('El dui no esta disponible.')
        return dui
    
    #formato de contraseña
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validar_password(password)
        return password

    #validacion  de contraseñas iguales
    def clean(self):
        clean_data = super().clean()
        password  = clean_data.get('password')
        password2 = clean_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2','Las contraseñas no coinciden.')
        return clean_data

#formulario para actulizar datos de empleado
class empleadoUpdateForm(forms.ModelForm):
    nombres = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombres',
            'autocomplete': 'off'})
    )
    apellidos = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellidos',
            'autocomplete': 'off'})
    )
    dui = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'DUI',
            'maxlength': '10',
            'autocomplete': 'off'}),validators=[validar_dui]
    )
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono',
            'maxlength': '9',
            'autocomplete': 'off'}),validators=[validar_telefono]
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario',
            'autocomplete': 'off'})
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico',
            'autocomplete': 'off'})
    )

    class Meta:
        model = CustomUser
        # Excluyendo campos de contraseña
        fields = ['nombres', 'apellidos', 'dui', 'telefono', 'username', 'email']
    
    #email unico
    def clean_email(self):
        email = self.cleaned_data.get('email')
        empleado_id = self.instance.idUsuario
        if CustomUser.objects.filter(email=email).exclude(idUsuario=empleado_id).exists():
            raise ValidationError('La direccion de correo electronico ya esta en uso.')
        return email
    
    #username unico
    def clean_username(self):
        username = self.cleaned_data.get('username')
        empleado_id = self.instance.idUsuario
        if CustomUser.objects.filter(username=username).exclude(idUsuario=empleado_id).exists():
            raise ValidationError('El nombre de usuario no esta disponible.')
        return username

    #dui unico
    def clean_dui(self):
        dui = self.cleaned_data.get('dui')
        empleado_id = self.instance.idUsuario
        if CustomUser.objects.filter(dui=dui).exclude(idUsuario=empleado_id).exists():
            raise ValidationError('El dui no esta disponible.')
        return dui

class ClienteForm(forms.ModelForm):
    duiCliente=forms.CharField(validators=[validar_dui])
    class meta:
        model= Cliente
        fields = [ 'nombreCliente', 'apellidoCliente', 'duiCliente', 'nacionalidadCliente','telefonoCliente','emailCliente']
        
