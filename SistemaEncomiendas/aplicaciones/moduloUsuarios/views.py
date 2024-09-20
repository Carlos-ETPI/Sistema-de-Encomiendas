
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import CustomUser,Repartidor, Cliente
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.views.generic import UpdateView,ListView,CreateView,UpdateView
from .forms import RepartidorForm, empleadoForm, empleadoUpdateForm, clienteForm, ClienteForm, clienteUpdateForm
from django.urls import reverse_lazy
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
CustomUser = get_user_model()
from .models import Cliente
from django.http import JsonResponse,HttpResponseBadRequest

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def group_required(group_name):
    def decorator(view_func):
        @login_required(login_url='seguridad_app:inicio_sesion')
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            return redirect('seguridad_app:noAccess')
        return _wrapped_view
    return decorator


#---------------------------Gestion de empleados---------------------------------
#Vista para listar empleados
class crud_empleados(ListView):
    model = CustomUser
    template_name = "moduloUsuarios/crudEmpleado.html"
    context_object_name = "lista_Empleados"

    def get_queryset(self):
        #filtrado de empleados (excluyendo super usarios y usuarios inactivos)
        return CustomUser.objects.filter(is_superuser=False, is_active=True).order_by('date_joined')

#vista para crear empleados
class crear_empleado(CreateView):
    form_class = empleadoForm
    success_url = reverse_lazy('moduloUsuarios:crud_empleado')
    template_name = 'moduloUsuarios/crearEmpleado.html'

#Elimanar empleados
def eliminar_empleado(request,pk):
    empleado = get_object_or_404(CustomUser, pk=pk)

    if request.method == "POST":
        try:
            empleado.delete()
            #mensaje de exito
            messages.success(request, 'Empleado eliminado correctamente!')
        except Exception as e:
            #mensaje de error
            messages.error(request, f'Error al eliminar el empleado: {str(e)}')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Empleado eliminado correctamente!'})
        return redirect("moduloUsuarios:crud_empleados")
    return render(request, "moduloUsuarios/eliminarEmpleado.html", {"empleado": empleado})

#vista inspeccionar usuario
def ver_empleado(request, pk):
    empleado = get_object_or_404(CustomUser, idUsuario=pk)
    return render(request, 'moduloUsuarios/ver_empleado.html',{'empleado':empleado})

class modificar_empleado(UpdateView):
    template_name = "moduloUsuarios/modificarEmpleado.html"
    model = CustomUser
    form_class = empleadoUpdateForm
    success_url = reverse_lazy("moduloUsuarios:crud_empleado")

    def form_valid(self, form):
        messages.success(self.request, "El empleado se ha modificado exitosamente")
        return super().form_valid(form)

#--------------------------- Modulo Repartidor----------------------
#vista crear
class crear_repartidor(CreateView):
    form_class = RepartidorForm
    success_url = reverse_lazy('moduloUsuarios:crud_repartidor')
    template_name = 'moduloUsuarios/crearRepartidor.html'

#vista listar repartidores
@method_decorator(group_required('Jefe'), name='dispatch')
class crud_repartidor(ListView):
    template_name = "moduloUsuarios/crudRepartidor.html"
    model = Repartidor
    context_object_name = "lista_Repartidor"
    # paginate_by=7
    # queryset=Repartidor.objects.all()

#vista ver datos repartidor
@group_required('Jefe')
def ver_repartidor(request, pk):
    repartidor = get_object_or_404(Repartidor, pk=pk)
    return render(
        request, "moduloUsuarios/verRepartidor.html", {"repartidor": repartidor}
    )

#vista modificar repartidor
@method_decorator(group_required('Jefe'), name='dispatch')
class modificar_repartidor(UpdateView):
    template_name = "moduloUsuarios/modificarRepartidor.html"
    model = Repartidor
    form_class = RepartidorForm
    success_url = reverse_lazy("moduloUsuarios:crud_repartidor")

    def form_valid(self, form):
        messages.success(self.request, "El Repartidor se ha modificado exitosamente")
        return super().form_valid(form)
    
#vista eliminar repartidor
@group_required('Jefe')
def eliminar_repartidor(request, pk):
    repartidor = get_object_or_404(Repartidor, pk=pk)

    if request.method == "POST":
        try:
            repartidor.delete()
            # Agregar mensaje de éxito
            messages.success(request, 'Repartidor eliminado correctamente!')
        except Exception as e:
            # Agregar mensaje de error si ocurre una excepción
            messages.error(request, f'Error al eliminar el repartidor: {str(e)}')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Repartidor eliminado correctamente!'})
        return redirect("moduloUsuarios:crud_repartidor")

    return render(request, "moduloUsuarios/eliminarRepartidor.html", {"repartidor": repartidor})
	
 
 #--------------------------- Modulo Gestion de Cliente Modificado----------------------
 #Vista para listar clientes
class crud_cliente(ListView):
    model = Cliente
    template_name = "moduloUsuarios/crudCliente.html"
    context_object_name = "lista_cliente"



#vista para crear clientes
class crear_cliente(CreateView):
    form_class = clienteForm
    success_url = reverse_lazy('moduloUsuarios:crud_cliente')
    template_name = 'moduloUsuarios/crearCliente.html'

#Eliminar cliente
def eliminar_cliente(request,pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == "POST":
        try:
            cliente.delete()
            #mensaje de exito
            messages.success(request, 'Cliente eliminado correctamente!')
        except Exception as e:
            #mensaje de error
            messages.error(request, f'Error al eliminar el cliente seleccionado: {str(e)}')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Cliente eliminado correctamente!'})
        return redirect("moduloUsuarios:crud_cliente")
    return render(request, "moduloUsuarios/eliminarEmpleado.html", {"cliente": cliente})

#vista inspeccionar Cliente
def ver_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'moduloUsuarios/inspeccionarCliente.html',{'cliente': cliente})


#Vista modificar datps cliente 
class modificar_cliente(UpdateView):
    template_name = "moduloUsuarios/modificarCliente.html"
    model = Cliente
    form_class = clienteUpdateForm
    success_url = reverse_lazy("moduloUsuarios:crud_cliente")

    def form_valid(self, form):
        messages.success(self.request, "El cliente seleccionado se ha modificado exitosamente")
        return super().form_valid(form)
