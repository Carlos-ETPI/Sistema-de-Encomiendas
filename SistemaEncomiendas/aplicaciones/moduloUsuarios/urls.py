from django.urls import path
from . import views
app_name = 'moduloUsuarios'
urlpatterns = [
    path('',views.crudUsuarios, name="users"),
    path('home/',views.home),
    path('agregar/',views.newuser, name="agregar"),
    path('create/',views.agregarUsuario, name="newuser"),
    path('ver/<int:pk>/',views.verUsuario, name="verUsuario"),
    path('inspeccionarUsuario/<int:pk>/',views.inspeccionarUsuario, name="inspeccionarUsuario"),
    path('modificar/',views.modUsuario, name="moduser"),
    path('eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    
     #Modulo de Gestion de Cliente 
    path('crudCliente/', views.crudClientes, name="crudClientes"),
    path('crearCliente/',views.agrClientes, name="agrCliente"),
    path('modificarCliente/',views.modClientes, name="modCliente"),
    path('eliminarCliente/',views.delCliente, name="delCliente"),
    path('verificarCliente/',views.verifCliente, name="verifCliente"),
    path('verCliente/',views.verCliente, name="verCliente"),



]