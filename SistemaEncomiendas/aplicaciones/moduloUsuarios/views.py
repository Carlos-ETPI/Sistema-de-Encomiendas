
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import CustomUser,Repartidor
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.views.generic import UpdateView,ListView,CreateView,UpdateView
from .forms import RepartidorForm, empleadoForm, empleadoUpdateForm
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


#Vistas para el submodulo de usuarios Gestion de Clientes 
#vista de crud Clientes

@group_required('Jefe')
def crudCliente(request):
    client_list = Cliente.objects.filter(estado=True)
    return render(request, 'moduloUsuarios/crudCliente.html', {'client_list': client_list})

#vista agregarCliente
@group_required('Jefe') 
def agregarClientes(request):
    if request.method == 'POST':
        # Recuperar los datos del formulario
        nombreCliente = request.POST['nombres']
        apellidoCliente = request.POST['apellidos']
        duiCliente = request.POST['dui']
        nacionalidadCliente = request.POST['nacionalidad']
        telefonoCliente = request.POST['telefono']
        emailCliente = request.POST['email']

        # Validaciones adicionales
        # No campos vacíos
        if not nombreCliente or not apellidoCliente or not duiCliente or not nacionalidadCliente or not telefonoCliente or not emailCliente:
            messages.error(request, 'Por favor complete todos los campos obligatorios')
            return render(request, 'moduloUsuarios/crearCliente.html')

        # Verificar que el DUI es único
        if Cliente.objects.filter(duiCliente=duiCliente).exists():
            messages.error(request, 'Error al ingresar documento de identidad, el número ingresado ya está registrado')
            return render(request, 'moduloUsuarios/crearCliente.html')

        # Verificar email
        if Cliente.objects.filter(emailCliente=emailCliente).exists():
            messages.error(request, 'La dirección de correo electrónico ya está en uso, por favor ingrese otro email')
            return render(request, 'moduloUsuarios/crearCliente.html')

        # Validación del formato del email
        try:
            validate_email(emailCliente)
        except ValidationError:
            messages.error(request, 'El formato del correo electrónico no es válido')
            return render(request, 'moduloUsuarios/crearCliente.html')

        # Validación de parámetros
        if len(nombreCliente) > 50:
            messages.error(request, 'Nombre demasiado extenso, trate de usar abreviaciones')
            return render(request, 'moduloUsuarios/crearCliente.html')

        if len(apellidoCliente) > 50:
            messages.error(request, 'Apellido demasiado extenso, trate de usar abreviaciones')
            return render(request, 'moduloUsuarios/crearCliente.html')

        if len(duiCliente) != 10:
            messages.error(request, 'Número de documento de identidad no válido')
            return render(request, 'moduloUsuarios/crearCliente.html')

        if len(telefonoCliente) != 9:
            messages.error(request, 'Número de teléfono no válido')
            return render(request, 'moduloUsuarios/crearCliente.html')

        try:
            # Creación de cliente
            cliente = Cliente.objects.create(
                nombreCliente=nombreCliente,
                apellidoCliente=apellidoCliente,
                duiCliente=duiCliente,
                nacionalidadCliente=nacionalidadCliente,
                telefonoCliente=telefonoCliente,
                emailCliente=emailCliente
            )
            return redirect('/usuarios/crudCliente')  # o cualquier otra página después del registro
        except Exception as e:
            messages.error(request, f'Error al crear el cliente: {str(e)}')
            return render(request, 'moduloUsuarios/crearCliente.html')
    else:
        return render(request, 'moduloUsuarios/crearCliente.html')

#renderizar html crearCliente
@group_required('Jefe')
def newCliente(request):
    return render(request, 'moduloUsuarios/crearCliente.html')

#Vista de formulario para modificar cliente
@group_required('Jefe')
def modificarClientes(request):
    if request.method == 'POST':
        pk = request.POST['idCliente']
        cliente = get_object_or_404(Cliente, idCliente=pk)
        cliente.nombreCliente = request.POST['nombres']
        cliente.apellidoCliente = request.POST['apellidos']
        cliente.duiCliente = request.POST['dui']
        cliente.nacionalidadCliente = request.POST['nacionalidad']
        cliente.telefonoCliente = request.POST.get('telefono')
        cliente.emailCliente = request.POST['email']

        # Validaciones
        # No campos vacíos
        if not cliente.nombreCliente or not cliente.apellidoCliente or not cliente.emailCliente or not cliente.duiCliente or not cliente.telefonoCliente or not cliente.nacionalidadCliente:
            messages.error(request, 'Por favor complete todos los campos obligatorios')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        # Verificar que el DUI es único
        if Cliente.objects.filter(duiCliente=cliente.duiCliente).exclude(idCliente=pk).exists():
            messages.error(request, 'Error al ingresar documento de identidad, el número ingresado ya está registrado')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        # Verificar email
        if Cliente.objects.filter(emailCliente=cliente.emailCliente).exclude(idCliente=pk).exists():
            messages.error(request, 'La dirección de correo electrónico ya está en uso, por favor ingrese otro email')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        # Validación del formato del email
        try:
            validate_email(cliente.emailCliente)
        except ValidationError:
            messages.error(request, 'El formato del correo electrónico no es válido')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        # Validación de parámetros
        if len(cliente.nombreCliente) > 50:
            messages.error(request, 'Nombre demasiado extenso, trate de usar abreviaciones')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        if len(cliente.apellidoCliente) > 50:
            messages.error(request, 'Apellido demasiado extenso, trate de usar abreviaciones')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        if len(cliente.duiCliente) != 10:
            messages.error(request, 'Número de documento de identidad no válido')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        if len(cliente.telefonoCliente) != 9:
            messages.error(request, 'Número de teléfono no válido')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        try:
            cliente.save()
            return redirect("/usuarios/crudCliente/")
        except Exception as e:
            messages.error(request, f'Error al modificar el cliente: {str(e)}')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})

    return redirect("/usuarios/crudCliente/")

#verificar cliente
@group_required('Jefe')
def verificarCliente(request, pk):
    cliente = get_object_or_404(Cliente, idCliente=pk)
    return render(request, 'moduloUsuarios/inspeccionarCliente.html', {'cliente': cliente})

#eliminar
@group_required('Jefe')
def deleteCliente(request, pk):
    cliente = get_object_or_404(Cliente, idCliente=pk)
    if request.method == 'POST':
        cliente.estado = False
        cliente.save()
        return redirect('/usuarios/crudCliente/')
    return render(request, 'moduloUsuarios/eliminarCliente.html',{'cliente':cliente})

#vista para ver usuario
@group_required('Jefe')
def verCliente(request, pk):
    cliente = get_object_or_404(Cliente, idCliente=pk)
    return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})


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
	