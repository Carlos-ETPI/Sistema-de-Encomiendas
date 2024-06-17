from django.urls import path
from . import views
app_name = 'moduloUsuarios'
urlpatterns = [
    path('',views.crudUsuarios, name="users"),
    path('agregar/',views.newuser, name="agregar"),
    path('create/',views.agregarUsuario, name="newuser"),
    path('ver/<int:pk>/',views.verUsuario, name="verUsuario"),
    path('inspeccionarUsuario/<int:pk>/',views.inspeccionarUsuario, name="inspeccionarUsuario"),
    path('modificar/',views.modUsuario, name="moduser"),
    path('eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    
     #Modulo de Gestion de Cliente 
    path('crudCliente/', views.crudCliente, name="crudCliente"),
    path('crearCliente/',views.agregarClientes, name="agregarCliente"),
    path('modificarCliente/',views.modificarClientes, name="modificarCliente"),
    path('eliminarCliente/',views.deleteCliente, name="deleteCliente"),
    path('verificarCliente/',views.verificarCliente, name="verificarCliente"),
    path('verCliente/',views.verCliente, name="verCliente"),



]