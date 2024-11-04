from django.urls import path
from . import views
app_name = 'moduloUsuarios'
urlpatterns = [
    #Vistas para empleados modificadas
    path("crud_empleado/", views.crud_empleados.as_view(), name="crud_empleado"),
    path("crear_empleado/", views.crear_empleado.as_view(),name="crear_empleado"),
    path("eliminar_empleado/<int:pk>/",views.eliminar_empleado,name="eliminar_empleado"),
    path('ver_empleado/<int:pk>/',views.ver_empleado, name="ver_empleado"),
    path('modificar_empleado/<int:pk>/',views.modificar_empleado.as_view(),name='modificar_empleado'),

     #Modulo de Gestion de Cliente 
    path('crudCliente/', views.crudCliente, name="crudCliente"),
    path('agregarCliente/',views.newCliente, name="newCliente"),
    path('crearCliente/',views.agregarClientes, name="agregarCliente"),
    path('modificarCliente/',views.modificarClientes, name="modificarCliente"),
    path('eliminarCliente/<int:pk>',views.deleteCliente, name="deleteCliente"),
    path('inspeccionarCliente/<int:pk>',views.verificarCliente, name="inspeccionarCliente"),
    path('verCliente/<int:pk>',views.verCliente, name="verCliente"),

    path("crear_repartidor/", views.crear_repartidor.as_view(), name="crear_repartidor"),
    path("crud_repartidor/", views.crud_repartidor.as_view(), name="crud_repartidor"),
    path("ver_repartidor/<int:pk>/", views.ver_repartidor, name="ver_repartidor"),
    path('modificar_repartidor/<int:pk>/', views.modificar_repartidor.as_view(), name='modificar_repartidor'),
    path( "eliminar_repartidor/<int:pk>/", views.eliminar_repartidor, name="eliminar_repartidor",),


]