from django.urls import path
from . import views

app_name = 'moduloSeguimiento'
urlpatterns = [
    path('cambiar-estado-paquete/', views.ListarEstados.as_view(), name='cambiar_estado'),
    path('crear-esado/<pk>/', views.CrearEstado.as_view(), name='crear_estado'),
    path('modificar-estado/', views.prueba_vista, name='modificarEstado'),
]
