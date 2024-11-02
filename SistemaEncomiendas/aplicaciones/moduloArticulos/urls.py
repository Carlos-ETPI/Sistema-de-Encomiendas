from django.urls import path
from . import views

app_name = 'moduloArticulos'

urlpatterns = [
    path('',views.registrar_articulo, name="registrarArticulo"),
    path('filtrarMarcas/', views.filtrar_marcas, name='filtrar_marcas'),
    path('filtrarTipoArticulo/', views.filtrar_tipo_articulo, name='filtrar_tipo_articulo'), 
    path('verArticulo/<int:pk>/', views.ver_articulo, name='ver_articulo'), 
]