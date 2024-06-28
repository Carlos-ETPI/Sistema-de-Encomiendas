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
    path('crudCliente/', views.crudClientes, name="crudClientes"),
    path('crearCliente/',views.agrClientes, name="agrCliente"),
    path('modificarCliente/',views.modClientes, name="modCliente"),
    path('eliminarCliente/',views.delCliente, name="delCliente"),
    path('verificarCliente/',views.verifCliente, name="verifCliente"),
    path('verCliente/',views.verCliente, name="verCliente"),

    path("crear_repartidor/", views.crear_repartidor.as_view(), name="crear_repartidor"),
    path("crud_repartidor/", views.crud_repartidor.as_view(), name="crud_repartidor"),
    path("ver_repartidor/<int:pk>/", views.ver_repartidor, name="ver_repartidor"),
    path('modificar_repartidor/<pk>/', views.modificar_repartidor.as_view(), name='modificar_repartidor'),
    path( "eliminar_repartidor/<pk>/", views.eliminar_repartidor, name="eliminar_repartidor",),


]