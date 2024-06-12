from django.urls import path
from . import views

urlpatterns = [
    path('',views.crudUsuarios, name="users"),
    path('agregar/',views.agregarUsuario, name="newuser"),
    path('ver/',views.verUsuario, name="checkuser"),
    path('modificar/',views.modUsuario, name="moduser"),
]