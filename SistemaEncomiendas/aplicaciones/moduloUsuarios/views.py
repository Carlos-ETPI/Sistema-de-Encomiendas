
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
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
    else:
        return render(request, 'moduloUsuarios/crud.html')
    
    return render(request, 'moduloUsuarios/crear.html')

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
        user.save()
        return redirect("/usuarios/")

#vista para ver usuario
@group_required('Jefe')
def verUsuario(request, pk):
    user = get_object_or_404(CustomUser, idUsuario=pk)
    return render(request, 'moduloUsuarios/modificar.html',{'user':user})

#eliminar
@group_required('Jefe')
def eliminar_usuario(request, pk):
    user = get_object_or_404(CustomUser, idUsuario=pk)
    user.delete()
    return redirect('/usuarios/')

