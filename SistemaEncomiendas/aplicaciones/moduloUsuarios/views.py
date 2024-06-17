from django.shortcuts import render, get_object_or_404, redirect
from .models import Repartidor
from .forms import RepartidorForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy
from django.contrib import messages

CustomUser = get_user_model()

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def group_required(group_name):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            return redirect("seguridad_app:noAccess")

        return _wrapped_view

    return decorator


# Vista de crud de usuarios
@group_required("Jefe")
def crudUsuarios(request):
    user_list = CustomUser.objects.filter(is_superuser=False).order_by("date_joined")
    return render(request, "moduloUsuarios/crud.html", {"user_list": user_list})


# Vista de formulario para agregar usuario
@group_required("Jefe")
def agregarUsuario(request):
    if request.method == "POST":
        # Recuperar los datos del formulario
        username = request.POST["username"]
        nombres = request.POST["nombres"]
        apellidos = request.POST["apellidos"]
        password = request.POST["password1"]
        email = request.POST["email"]
        dui = request.POST.get("dui")  # Puede ser None si no se proporciona
        telefono = request.POST.get("telefono")

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            dui=dui,
            telefono=telefono,
            nombres=nombres,
            apellidos=apellidos,
        )

        return redirect("/usuarios/")  # o cualquier otra página después del registro
    else:
        return render(request, "moduloUsuarios/crud.html")

    return render(request, "moduloUsuarios/crear.html")


# template agregar
@group_required("Jefe")
def newuser(request):
    return render(request, "moduloUsuarios/crear.html")


# vista de modificar usuario
@group_required("Jefe")
def modUsuario(request):
    if request.method == "POST":
        pk = request.POST["id"]
        user = get_object_or_404(CustomUser, idUsuario=pk)
        user.nombres = request.POST["nombres"]
        user.apellidos = request.POST["apellidos"]
        user.dui = request.POST["dui"]
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.telefono = request.POST.get("telefono")
        user.save()
        return redirect("/usuarios/")


# vista para ver usuario
@group_required("Jefe")
def verUsuario(request, pk):
    user = get_object_or_404(CustomUser, idUsuario=pk)
    return render(request, "moduloUsuarios/modificar.html", {"user": user})


# eliminar
@group_required("Jefe")
def eliminar_usuario(request, pk):
    user = get_object_or_404(CustomUser, idUsuario=pk)
    user.delete()
    return redirect("/usuarios/")


# Vistas para el submodulo de usuarios Gestion de Clientes
# vista de crud Clientes
def crudClientes(request):
    return render(request, "moduloUsuarios/crudCliente.html")


def agrClientes(request):
    return render(request, "moduloUsuarios/crearCliente.html")


# Vista de formulario para agregar usuario
def modClientes(request):
    return render(request, "moduloUsuarios/modificarCliente.html")


# verificar cliente
def verifCliente(request):
    return render(request, "moduloUsuarios/verificarCliente.html")


# eliminar
def delCliente(request):

    return render(request, "moduloUsuarios/eliminarCliente.html")


# vista para ver usuario
def verCliente(request):
    return render(request, "moduloUsuarios/verCliente.html")


# Modulo Repartidor
# Vistas de repartidor


def crear_repartidor(request):
    if request.method == "POST":
        form = RepartidorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("moduloUsuarios:crud_repartidor")
    else:
        form = RepartidorForm()
    return render(request, "moduloUsuarios/crearRepartidor.html", {"form": form})


class crud_repartidor(ListView):
    template_name = "moduloUsuarios/crudRepartidor.html"
    model = Repartidor
    context_object_name = "lista_Repartidor"
    # paginate_by=7
    # queryset=Repartidor.objects.all()


def ver_repartidor(request, pk):
    repartidor = get_object_or_404(Repartidor, pk=pk)
    return render(
        request, "moduloUsuarios/verRepartidor.html", {"repartidor": repartidor}
    )


class modificar_repartidor(UpdateView):
    template_name = "moduloUsuarios/modificarRepartidor.html"
    model = Repartidor
    form_class = RepartidorForm
    success_url = reverse_lazy("moduloUsuarios:crud_repartidor")

    def form_valid(self, form):
        messages.success(self.request, "El Repartidor se ha modificado exitosamente")
        return super().form_valid(form)


def eliminar_repartidor(request, pk):
    repartidor = get_object_or_404(Repartidor, pk=pk)

    if request.method == "POST":
        repartidor.delete()
        return redirect("moduloUsuarios:crud_repartidor")

    return render(
        request, "moduloUsuarios/eliminarRepartidor.html", {"repartidor": repartidor}
    )
