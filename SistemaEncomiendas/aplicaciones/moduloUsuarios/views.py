from django.shortcuts import render

# Create your views here.

#Vista de crud de usuarios
def crudUsuarios(request):
    return render(request, 'moduloUsuarios/crud.html')

#Vista de formulario para agregar usuario
def agregarUsuario(request):
    return render(request, 'moduloUsuarios/crear.html')

#vista de modificar usuario
def modUsuario(request):
    return render(request, 'moduloUsuarios/modificar.html')

#vista para ver usuario
def verUsuario(request):
    return render(request, 'moduloUsuarios/ver.html')