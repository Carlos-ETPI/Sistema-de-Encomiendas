from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario',max_length=50, required=True)
    password = forms.CharField(label='Clave', max_length=100, required=True,widget=forms.PasswordInput)