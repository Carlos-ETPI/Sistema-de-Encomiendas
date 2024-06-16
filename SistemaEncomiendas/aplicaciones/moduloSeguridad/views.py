from django.shortcuts import render
from django.shortcuts import redirect
from .forms import LoginForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.
def no_access_view(request):
    return render(request, 'moduloSeguridad/accesoDen.html')

def crud(request):
    return render(request,'moduloSeguridad/crud.html')

def registro(request):
    return render(request,'moduloSeguridad/registro.html')

class LoginUser(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('moduloUsuarios:users')
    template_name = 'moduloSeguridad/login.html'
    def form_valid(self, form):
        credenciales = form.cleaned_data
        user = authenticate(username=credenciales['username'],password=credenciales['password'])
        
        if user is not None:
            login(self.request, user)
            if self.request.GET:
                next = self.request.GET['next']
                return redirect(next)
            return redirect(self.success_url)
        else:
                messages.add_message(self.request, messages.WARNING,'Error: credenciales incorrectas ')
                return redirect(reverse_lazy('seguridad_app:inicio_sesion'))

def cerrar_sesion(request):
    logout(request)
    return redirect(reverse_lazy('seguridad_app:CRUD'))

class ChangePasswordView(FormView):
    template_name = 'moduloseguridad/cambiarContraseña.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('seguridad_app:CRUD')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)  
        messages.success(self.request, 'Tu contraseña ha sido actualizada correctamente.')
        return super().form_valid(form)
