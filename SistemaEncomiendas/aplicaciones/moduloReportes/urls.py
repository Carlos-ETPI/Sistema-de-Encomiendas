from django.urls import path
from . import views

app_name = 'moduloReportes'
urlpatterns = [
    path('reporte-costos-viajes/', views.reporte_costos_viajes, name='reporte_costos_viajes'),
    path('pdf-reporte-costos-viajes/', views.pdf_reporte_costos_viajes, name='pdf_reporte_costos_viajes'),
]
