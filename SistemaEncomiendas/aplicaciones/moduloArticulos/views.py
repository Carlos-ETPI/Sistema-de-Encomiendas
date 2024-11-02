from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import CrearArticuloForm
from .models import Articulo
from .models import TipoArticulo
from .models import Servicio
from .models import Cancelacion
from .models import ListadoImpuesto
from .models import ListadoMarcas


# Create your views here.
# Vista para mostrar el formulario de registro de articulo
#@group_required('Jefe')
def registrar_articulo(request):
    mensaje = None     #Mensaje de validacion
    servicios_list=Servicio.objects.all()
    
    if request.method == 'POST':
        
        id_servicio = request.POST.get('id_servicio')
        categoria_articulo_id = request.POST.get('id_ti_articulo')
        marca_id = request.POST.get('id_lis_marcas')
        nombre_articulo = request.POST.get('nombre_articulo')
        cantidad = request.POST.get('cantidad')
        peso = request.POST.get('peso')


        articulo = Articulo(
            id_servicio_id=id_servicio,
            id_ti_articulo_id=categoria_articulo_id,
            id_lis_marcas_id=marca_id,
            nombre_articulo=nombre_articulo,
            cantidad=cantidad,
            peso=peso,
            estado = "Sin estado",
            impuestos_envio = 0,
            costo_encomienda = 0,
            costo_total_envio = 0,
        )

        # Guardar el nuevo artículo en la base de datos
        articulo.save()
    return render(request, 'moduloArticulos/crearArticulo.html', {'mensaje':mensaje, 'servicios':servicios_list})

# Vista para filtrar las marcas
def filtrar_marcas(request):
    tipo = request.GET.get('tipo_marca')
    marcas = ListadoMarcas.objects.filter(tipo_marca=tipo)
    marcas_data = [{'id': marca.id_lis_marcas, 'nombre': marca.nombre_marca} for marca in marcas]
    return JsonResponse(marcas_data, safe=False)

# Vista para filtrar las tipo de articulo
def filtrar_tipo_articulo(request):
    tipo = request.GET.get('tipo_marca')
    categoria = request.GET.get('catego')
    articulos = TipoArticulo.objects.filter(categoria_tipo=categoria, tipo_marca=tipo)
    articulo_data = [{'id': articulo.id_ti_articulo, 'nombre': articulo.nombre_tipo} for articulo in articulos]
    return JsonResponse(articulo_data, safe=False)

# Vista para ver un articulo
def ver_articulo(request,pk):
    articulo = get_object_or_404(Articulo, id_articulo=pk)
    return render(request, 'moduloArticulos/verArticulo.html',{'articulo':articulo})
