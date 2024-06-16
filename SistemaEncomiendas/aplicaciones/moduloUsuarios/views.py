
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
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
            return redirect('seguridad_app:noAccess')
        return _wrapped_view
    return decorator


#Vista de crud de usuarios
@group_required('Jefe')
def crudUsuarios(request):
    user_list = CustomUser.objects.filter(is_superuser=False).order_by('date_joined')
    return render(request, 'moduloUsuarios/crud.html', {'user_list': user_list})

#Vista de formulario para agregar usuario
@group_required('Jefe')
def agregarUsuario(request):
    if request.method == 'POST':
        # Recuperar los datos del formulario
        username = request.POST['username']
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        password = request.POST['password1']
        email = request.POST['email']
        dui = request.POST.get('dui')  # Puede ser None si no se proporciona
        telefono = request.POST.get('telefono')
        password2= request.POST['password2']

        #validaciones adicionales
        #No campos vacios
        if not username or not nombres or not apellidos or not password or not email or not dui or not telefono or not password2:
            messages.error(request, 'Por favor complete todos los campos obligatorios')
            return render(request, 'moduloUsuarios/crear.html')
        
        #verificar nombre de usuario existente
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Este nombre de usuario ya existe, por favor ingrese uno distinto')
            return render(request, 'moduloUsuarios/crear.html')
        
        #verificar emial
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'La direccion de correo electronica ya esta en uso, por favor ingrese otro email')
            return render(request, 'moduloUsuarios/crear.html')
        
        #validacion de parametros
        if len(nombres) > 50:
            messages.error(request, 'Nombres demasiado extensos, trate de usar abreviaciones como: David G. Aguilar')
            return render(request, 'moduloUsuarios/crear.html')
        
        if len(apellidos) > 50:
            messages.error(request, 'Apellidos demasiado extensos, trate de usar abreviaciones como: G. Aguilar')
            return render(request, 'moduloUsuarios/crear.html')
        
        if len(dui) > 10:
            messages.error(request, 'Numero de documento de identidad no valido')
            return render(request, 'moduloUsuarios/crear.html')
        
        if len(telefono) > 10:
            messages.error(request, 'Numero de telefono no valido')
            return render(request, 'moduloUsuarios/crear.html')
        
        #validacion de contraseñas
        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'moduloUsuarios/crear.html')
        
        try:
            #creacion de usuario
            user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            dui=dui,
            telefono=telefono,
            nombres=nombres,
            apellidos=apellidos
            )
            return redirect('/usuarios/')  # o cualquier otra página después del registro
        except Exception as e:
            messages.error(request, f'Error al crear el usuario: {str(e)}')
            return render(request, 'moduloUsuarios/crear.html')
    else:
        return render(request, 'moduloUsuarios/crear.html')
        #return render(request, 'moduloUsuarios/crud.html')
    

    #return render(request, 'moduloUsuarios/crear.html')

#template agregar
@group_required('Jefe')
def newuser(request):
    return render(request, 'moduloUsuarios/crear.html')

#vista de modificar usuario
@group_required('Jefe')
def modUsuario(request):
    if request.method == 'POST':
        pk=request.POST['id']
        user = get_object_or_404(CustomUser, idUsuario=pk)
        user.nombres = request.POST['nombres']
        user.apellidos = request.POST['apellidos']
        user.dui = request.POST['dui']
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.telefono = request.POST.get('telefono')

        #validaciones
        #No campos vacios
        if not user.username or not user.nombres or not user.apellidos or not user.email or not user.dui or not user.telefono:
            messages.error(request, 'Por favor complete todos los campos obligatorios')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        #verificar nombre de usuario existente
        if CustomUser.objects.filter(username=user.username).exclude(idUsuario=pk).exists():
            messages.error(request, 'Este nombre de usuario ya existe, por favor ingrese uno distinto')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        #verificar emial
        if CustomUser.objects.filter(email=user.email).exclude(idUsuario=pk).exists():
            messages.error(request, 'La direccion de correo electronica ya esta en uso, por favor ingrese otro email')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        #validacion de parametros
        if len(user.nombres) > 50:
            messages.error(request, 'Nombres demasiado extensos, trate de usar abreviaciones como: David G. Aguilar')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        if len(user.apellidos) > 50:
            messages.error(request, 'Apellidos demasiado extensos, trate de usar abreviaciones como: G. Aguilar')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        if len(user.dui) > 10:
            messages.error(request, 'Numero de documento de identidad no valido')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        if len(user.telefono) > 10:
            messages.error(request, 'Numero de telefono no valido')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        try:
            user.save()
            return redirect("/usuarios/")
        except Exception as e:
            messages.error(request, f'Error al modificar el usuario: {str(e)}')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
    return redirect("/usuarios/")

#vista para ver usuario
@group_required('Jefe')
def verUsuario(request, pk):
    user = get_object_or_404(CustomUser, idUsuario=pk)
    return render(request, 'moduloUsuarios/modificar.html',{'user':user})

#vista inspeccionar usuario
@group_required('Jefe')
def inspeccionarUsuario(request, pk):
    user = get_object_or_404(CustomUser, idUsuario=pk)
    return render(request, 'moduloUsuarios/inspeccionarUsuario.html',{'user':user})

#eliminar
@group_required('Jefe')
def eliminar_usuario(request, pk):
    user = get_object_or_404(CustomUser, idUsuario=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('/usuarios/')
    return render(request,'moduloUsuarios/eliminarUsuario.html',{'user':user})
    
def home(request):
    return render(request,'home.html')

#Vistas para el submodulo de usuarios Gestion de Clientes 
#vista de crud Clientes
def crudClientes(request):
    return render(request,'moduloUsuarios/crudCliente.html')

def agrClientes(request):
    return render(request,'moduloUsuarios/crearCliente.html')

#Vista de formulario para agregar usuario
def modClientes(request):
    return render(request,'moduloUsuarios/modificarCliente.html')

#verificar cliente
def verifCliente(request):
    return render(request, 'moduloUsuarios/verificarCliente.html')

#eliminar
def delCliente(request):

    return render(request, 'moduloUsuarios/eliminarCliente.html')

#vista para ver usuario
def verCliente(request):
    return render(request, 'moduloUsuarios/verCliente.html')