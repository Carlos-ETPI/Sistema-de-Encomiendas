from django.urls import path
from . import views
app_name = 'moduloEntRec'
urlpatterns = [
    path('listar_rutas/',views.ListarRuta.as_view(), name="ListarRutas"),
    path('crear_ruta/',views.CrearRuta.as_view(), name="CrearRuta"),
    path('editar_ruta/<int:pk>/',views.EditarRuta.as_view(), name="EditarRuta"),
    path( "eliminar_ruta/<int:pk>/", views.EliminarRuta, name="EliminarRuta",),
    path('ver_ruta/<int:pk>/',views.VerRuta.as_view(), name="VerRuta"),

]