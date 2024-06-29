from django.urls import path
from . import views


urlpatterns = [
    path('nuevo/',views.nuevoviaje, name="nuevoviaje"),
    path('editar/',views.editarviaje, name="editarviaje"),
    path('',views.mostrarviajes, name="listaviajes"),
]