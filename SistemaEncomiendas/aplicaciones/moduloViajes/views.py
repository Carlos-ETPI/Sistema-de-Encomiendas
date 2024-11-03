from django.shortcuts import render, redirect,get_object_or_404
from .forms import CrearViajeForm
from .models import Viaje
from django.http import HttpResponse, HttpRequest,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def group_required(group_name):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            return redirect('seguridad_app:noAccess')
        return _wrapped_view
    return decorator

# Vista para mostrar el listado de viajes ordenados segun el id
@group_required('Jefe')
def mostrar_viajes(request):
    viajes_list = Viaje.objects.all().order_by('id_viaje') 
    return render(request, 'moduloViajes/viajes.html', {'viajes': viajes_list})


# Vista para mostrar el listado de viajes filtrados por el destino
@group_required('Jefe')
def mostrar_viajes_filtrados(request):
    if request.method == 'POST':
        destino = request.POST.get('destino', '')
        viajes_list = Viaje.objects.filter(destino=destino).order_by('fecha_ida')
    else:
        viajes_list = Viaje.objects.all().order_by('fecha_ida')
    
    
    return render(request, 'moduloViajes/viajes.html', {'viajes': viajes_list})


 #Vista para mostrar los datos de un viaje
@group_required('Jefe')
def ver_viaje(request,pk):
    viaje = get_object_or_404(Viaje, id_viaje=pk)
    viaje.precio_boleto_ida = str(viaje.precio_boleto_ida).replace(',', '.')
    viaje.precio_boleto_retorno = str(viaje.precio_boleto_retorno).replace(',', '.')
    
    return render(request, 'moduloViajes/verViaje.html',{'viaje':viaje})


# Vista para crear un nuevo viaje
@group_required('Jefe')
def crear_viaje(request):
    mensaje = None     #Mensaje de validacion
    if request.method == 'POST':
        form = CrearViajeForm(request.POST)         #Se crea el formulario (definido en forms.py)
        if form.is_valid():
            form.save()
            mensaje='registro exitoso'
        else:
            print(f'Formulario no válido: {form.errors}')    # si hay un error lo muestra en consola
    else:
        form = CrearViajeForm()  # Mueve esta línea fuera del else
    return render(request, 'moduloViajes/crearViaje.html', {'form': form, 'mensaje':mensaje})



# Vista para editar un viaje
@group_required('Jefe')
def editar_viaje(request,pk):
    viaje = get_object_or_404(Viaje, id_viaje=pk)
    viaje.precio_boleto_ida = str(viaje.precio_boleto_ida).replace(',', '.')
    viaje.precio_boleto_retorno = str(viaje.precio_boleto_retorno).replace(',', '.')

    if request.method == 'POST':
        viaje.fecha_ida = request.POST['fecha_ida']
        viaje.fecha_vuelta = request.POST['fecha_vuelta']
        viaje.destino = request.POST['destino']
        viaje.cantidad_personas= request.POST['cantidad_personas']
        viaje.precio_boleto_ida = request.POST['precio_boleto_ida']
        viaje.precio_boleto_retorno= request.POST['precio_boleto_retorno']
            
        viaje.save()
        return redirect('/viajes/')
    return render(request, 'moduloViajes/editarViaje.html',{'viaje':viaje})
    
# Metodo para eliminar un viaje
@group_required('Jefe')
def eliminar_viaje(request, pk):
    viaje = get_object_or_404(Viaje, id_viaje=pk)
    
    if request.method == "POST":
        try:
            viaje.delete()
            # Agregar mensaje de éxito
            messages.success(request, 'Viaje eliminado correctamente!')
        except Exception as e:
            # Agregar mensaje de error si ocurre una excepción
            messages.error(request, f'Error al eliminar el viaje: {str(e)}')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Viaje eliminado correctamente!'})
        return redirect("moduloViajes:listaviajes")

    return render(request, "moduloViajes/viajes.html", {"viaje": viaje})
    


