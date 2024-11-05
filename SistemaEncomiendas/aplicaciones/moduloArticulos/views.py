from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal
from .models import Articulo
from .models import Articulo_Auxiliar
from .models import TipoArticulo
from .models import Servicio
from .models import Cancelacion
from .models import ListadoMarcas



def mostrar_articulos(request):
    articulos_list = Articulo.objects.all()
    
    for articulo in articulos_list:
        # Obtener el nombre del servicio relacionado con el id_servicio de cada Articulo
        servicio = Servicio.objects.filter(id_servicio=articulo.id_servicio_id).first()
        articulo.nombre_servicio = servicio.nombre_servicio
    
    return render(request, 'moduloArticulos/listaArticulos.html', {'articulos': articulos_list})

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

        servicio = Servicio.objects.get(id_servicio=id_servicio)
        tipo=TipoArticulo.objects.get(id_ti_articulo=categoria_articulo_id)
        
        costoEncomiendas = servicio.precio_libra * Decimal(peso)
        impuestos=tipo.cip*Decimal(0.13)
        totalcosto=costoEncomiendas+impuestos


        articulo = Articulo(
            id_servicio_id=id_servicio,
            id_ti_articulo_id=categoria_articulo_id,
            id_lis_marcas_id=marca_id,
            nombre_articulo=nombre_articulo,
            cantidad=cantidad,
            peso=peso,
            estado = "Sin estado",
            impuestos_envio = impuestos,
            costo_encomienda = costoEncomiendas,
            costo_total_envio = totalcosto,
        )

        
        # Guardar el nuevo artículo en la base de datos
        articulo.save()
        messages.success(request, 'Articulo agregado correctamente!')
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
    servicio=articulo.id_servicio
    tipo = articulo.id_ti_articulo
    marca = articulo.id_lis_marcas
    return render(request, 'moduloArticulos/verArticulo.html',{'articulo':articulo,'servicio':servicio,'tipo_art':tipo,'marca':marca})


def editar_articulo(request,pk):
    articulo = get_object_or_404(Articulo, id_articulo=pk)
    articulo.peso = str(articulo.peso).replace(',', '.')
    articulo.costo_encomienda = str(articulo.costo_encomienda).replace(',', '.')
    articulo.costo_total_envio = str(articulo.costo_total_envio).replace(',', '.')


    servicio=articulo.id_servicio
    tipo = articulo.id_ti_articulo
    marca = articulo.id_lis_marcas

    if request.method == 'POST':
        
        articulo.nombre_articulo = request.POST.get('nombre_articulo')
        articulo.cantidad = request.POST.get('cantidad')
        articulo.peso = request.POST.get('peso')
        articulo.costo_encomienda= request.POST.get('costo_encomiendas')
        
        totalcosto=articulo.impuestos_envio+Decimal(articulo.costo_encomienda)
        articulo.costo_total_envio = totalcosto

        # Guardar el nuevo artículo en la base de datos
        articulo.save()
        messages.success(request, 'El Articulo se ha editado correctamente!')
    return render(request, 'moduloArticulos/editarArticulo.html',{"articulo": articulo,'servicio':servicio,'tipo_art':tipo,'marca':marca})




def eliminar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, id_articulo=pk)
    
    if request.method == "POST":
        try:
            articulo.delete()
            # Agregar mensaje de éxito
            messages.success(request, 'Articulo eliminado correctamente!')
        except Exception as e:
            # Agregar mensaje de error si ocurre una excepción
            messages.error(request, f'Error al eliminar el articulo: {str(e)}')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Articulo eliminado correctamente!'})
        return redirect("moduloArticulo:mostrar_articulos")

    return render(request, "moduloArticulos/listaArticulos.html", {"articulo": articulo})



def cotizacion(request):
    mensaje = None     #Mensaje de validacion
    servicios_list=Servicio.objects.all()
    
    if request.method == 'POST':
        
        id_servicio = request.POST.get('id_servicio')
        categoria_articulo_id = request.POST.get('id_ti_articulo') or None
        marca_id = request.POST.get('id_lis_marcas') or None
        nombre_articulo = request.POST.get('nombre_articulo')
        cantidad = request.POST.get('cantidad')
        peso = request.POST.get('peso')
        costo = request.POST.get('costoenco')


        servicio = Servicio.objects.get(id_servicio=id_servicio)
        tipo=None
        impuestos=Decimal(costo)*Decimal(0.13)
        if categoria_articulo_id:
            tipo=TipoArticulo.objects.get(id_ti_articulo=categoria_articulo_id)
            impuestos=tipo.cip*Decimal(0.13)
        
        costoEncomiendas = servicio.precio_libra * Decimal(peso) + Decimal(costo)
        totalcosto=costoEncomiendas+impuestos

        
        articulo = Articulo_Auxiliar(
            id_servicio_id=id_servicio,
            id_ti_articulo_id=categoria_articulo_id,
            id_lis_marcas_id=marca_id,
            nombre_articulo=nombre_articulo,
            cantidad=cantidad,
            peso=peso,
            estado = "Sin estado",
            impuestos_envio = impuestos,
            costo_encomienda = costoEncomiendas,
            costo_total_envio = totalcosto,
        )

        
        # Guardar el nuevo artículo en la base de datos
        articulo.save()
        messages.success(request, 'Cotizacion exitosa!')
        return redirect('/articulos/cotizacion/vista')
    return render(request, 'moduloArticulos/cotizacion.html', {'mensaje':mensaje, 'servicios':servicios_list})


def ver_cotizacion(request):
    articulo = Articulo_Auxiliar.objects.first()
    servicio=articulo.id_servicio
    tipo = articulo.id_ti_articulo
    marca = articulo.id_lis_marcas
    return render(request, 'moduloArticulos/vercotizacion.html',{'articulo':articulo,'servicio':servicio,'tipo_art':tipo,'marca':marca})

def eliminar_cotizacion(request):
    articulo = Articulo_Auxiliar.objects.first()
    articulo.delete()
    return redirect('/articulos/cotizacion/')
    