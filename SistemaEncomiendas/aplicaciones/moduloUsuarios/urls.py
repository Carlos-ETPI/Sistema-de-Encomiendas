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

    #Modulo de Gestion de Cliente Modificada
    path('crud_cliente/', views.crud_cliente.as_view(), name="crud_cliente"),
    path('crear_cliente/',views.crear_cliente.as_view(), name="crear_cliente"),
    path('modificar_cliente/<int:pk>/',views.modificar_cliente.as_view(), name="modificar_cliente"),
    path("eliminar_cliente/<int:pk>/",views.eliminar_cliente, name="eliminar_cliente"),
    path('ver_cliente/<int:pk>/',views.ver_cliente, name="ver_cliente"), 
     


    #Modulo de GRepartidores
    path("crear_repartidor/", views.crear_repartidor.as_view(), name="crear_repartidor"),
    path("crud_repartidor/", views.crud_repartidor.as_view(), name="crud_repartidor"),
    path("ver_repartidor/<int:pk>/", views.ver_repartidor, name="ver_repartidor"),
    path('modificar_repartidor/<int:pk>/', views.modificar_repartidor.as_view(), name='modificar_repartidor'),
    path( "eliminar_repartidor/<int:pk>/", views.eliminar_repartidor, name="eliminar_repartidor"),


]