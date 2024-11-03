from django.urls import path
from . import views

app_name = 'moduloArticulos'

urlpatterns = [
    path('',views.registrar_articulo, name="registrarArticulo"),
    path('cotizacion/',views.cotizacion, name="cotizacion"),
    path('cotizacion/vista',views.ver_cotizacion, name="ver_cotizacion"),
    path('eliminar/', views.eliminar_cotizacion, name='eliminar_cotizacion'),
    path('filtrarMarcas/', views.filtrar_marcas, name='filtrar_marcas'),
    path('filtrarTipoArticulo/', views.filtrar_tipo_articulo, name='filtrar_tipo_articulo'), 
    path('lista/', views.mostrar_articulos, name='mostrar_articulos'),
    path('<int:pk>/', views.ver_articulo, name='ver_articulo'),
    path('editar/<int:pk>/', views.editar_articulo, name='editar_articulo'), 
    path('eliminar/<int:pk>/', views.eliminar_articulo, name='eliminar_articulo'),
]