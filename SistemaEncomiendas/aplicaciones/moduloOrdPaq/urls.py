from django.urls import path
from . import views
app_name = 'moduloOrdPaq'

#Listado de urls
urlpatterns = [
    #vistas para pedidos
    path("crudPedido/", views.crudPedido.as_view(),name="crudPedido"),
    path("crearPedido/", views.crearPedido.as_view(), name="crearPedido"),
    path("modificarPedido/<int:pk>/",views.modificarPedido.as_view(),name="modificarPedido"),
    path("eliminarPedido/<int:pk>/",views.eliminarPedido,name="eliminarPedido"),
    path('verPedido/<int:pk>/',views.verPedido,name="verPedido"),
]