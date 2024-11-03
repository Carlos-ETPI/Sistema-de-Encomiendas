# views.py
from django.shortcuts import render,redirect
from django.http import HttpResponse
from aplicaciones.moduloViajes.models import Viaje
from weasyprint import HTML
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth
from django.contrib import messages 
import json
from ..moduloUsuarios .views import group_required

@group_required('Jefe')
def reporte_costos_viajes(request):

    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        if not fecha_inicio or not fecha_fin:
            messages.error(request, "Por favor ingresa ambas fechas de inicio y fin.")
            return render(request, 'moduloReportes/reporte_costo_viaje.html')
        # Total de costos en el intervalo de fechas
        total_costos = Viaje.objects.filter(
            fecha_ida__range=[fecha_inicio, fecha_fin]
        ).aggregate(total=Sum(
            F('precio_boleto_ida') * F('cantidad_personas') +
            F('precio_boleto_retorno') * F('cantidad_personas')
        ))['total'] 
        
        # Costo total agrupado por mes en el intervalo
        costos_por_mes = Viaje.objects.filter(
            fecha_ida__range=[fecha_inicio, fecha_fin]
        ).annotate(month=TruncMonth('fecha_ida')).values('month').annotate(
            total_mes=Sum(
                F('precio_boleto_ida') * F('cantidad_personas') +
                F('precio_boleto_retorno') * F('cantidad_personas')
            )
        ).order_by('month')

        # Mes con el costo más alto y más bajo
        mes_costo_mas_alto = costos_por_mes.order_by('-total_mes').first()
        mes_costo_mas_bajo = costos_por_mes.order_by('total_mes').first()

        # Cantidad total de viajes en el intervalo de fechas
        cantidad_viajes = Viaje.objects.filter(
            fecha_ida__range=[fecha_inicio, fecha_fin]
        ).count()

        # Consulta de viajes usando las fechas obtenidas
        viajes = Viaje.objects.filter(fecha_ida__range=[fecha_inicio, fecha_fin])
    else:
        # Total de costos sin aplicar filtros de fechas
        total_costos = Viaje.objects.aggregate(
            total=Sum(F('precio_boleto_ida') * F('cantidad_personas') + F('precio_boleto_retorno') * F('cantidad_personas'))
        )['total']

        # Costo total agrupado por mes sin filtrar por fecha
        costos_por_mes = Viaje.objects.annotate(month=TruncMonth('fecha_ida')).values('month').annotate(
            total_mes=Sum(F('precio_boleto_ida') * F('cantidad_personas') + F('precio_boleto_retorno') * F('cantidad_personas'))
        ).order_by('month')

        # Mes con el costo más alto y más bajo sin filtrar por fecha
        mes_costo_mas_alto = costos_por_mes.order_by('-total_mes').first()
        mes_costo_mas_bajo = costos_por_mes.order_by('total_mes').first()

        # Cantidad total de viajes sin filtrar por fecha
        cantidad_viajes = Viaje.objects.count()

        # Consulta de viajes (todos los viajes)
        viajes = Viaje.objects.all() 

    #Datos de Costos mas altos y bajos por mes
    grap= Viaje.objects.annotate(month=TruncMonth('fecha_ida')).values('month').annotate(
        total_mes=Sum(F('precio_boleto_ida') * F('cantidad_personas') +
                      F('precio_boleto_retorno') * F('cantidad_personas'))
    ).order_by('month')
    print(grap)
    
    labels = [item['month'].strftime('%B %Y') for item in grap] 
    data_max = [float(item['total_mes'] ) for item in costos_por_mes] 
    data_min = [float(item['total_mes'] ) for item in costos_por_mes]
    
    # Datos de viajes por mes
    viajes_por_mes = (
        Viaje.objects
        .annotate(month=TruncMonth('fecha_ida'))
        .values('month')
        .annotate(count=Count('id_viaje'))
        .order_by('month')
    )

    # Preparar los datos para el gráfico
    labels_g2 = [viaje['month'].strftime('%B %Y') for viaje in viajes_por_mes]
    data_g2 = [viaje['count'] for viaje in viajes_por_mes]
    
    # Cálculo de costos
    for viaje in viajes:
        viaje.costo_total_ida = viaje.precio_boleto_ida * viaje.cantidad_personas
        viaje.costo_total_vuelta = viaje.precio_boleto_retorno * viaje.cantidad_personas
        viaje.costo_total = viaje.costo_total_ida + viaje.costo_total_vuelta
    
    # Renderizar el template con los viajes
    return render(request, 'moduloReportes/reporte_costo_viaje.html', 
            {'viajes': viajes,
            'total_costos': total_costos,
            'mes_costo_mas_alto': mes_costo_mas_alto,
            'mes_costo_mas_bajo': mes_costo_mas_bajo,
            'cantidad_viajes': cantidad_viajes,
            'labels': json.dumps(labels),
            'data_max': json.dumps(data_max),
            'data_min': json.dumps(data_min),
            'labels_g2': json.dumps(labels_g2),
            'data_g2': json.dumps(data_g2)})
    
    
    

@group_required('Jefe')
def pdf_reporte_costos_viajes(request):
    # Obtener todos los viajes
    viajes = Viaje.objects.all()

    # Calcular el costo total para cada viaje
    for viaje in viajes:
        viaje.costo_total_ida = viaje.precio_boleto_ida * viaje.cantidad_personas
        viaje.costo_total_vuelta = viaje.precio_boleto_retorno * viaje.cantidad_personas
        viaje.costo_total = viaje.costo_total_ida + viaje.costo_total_vuelta

    # Renderizar el HTML de la plantilla para el PDF
    html_string = render_to_string('moduloReportes/pdf_reporte_costos_por_viaje.html', {'viajes': viajes})

    # Generar el PDF
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # Enviar el PDF como respuesta
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte_costos_viajes.pdf"'

    return response
