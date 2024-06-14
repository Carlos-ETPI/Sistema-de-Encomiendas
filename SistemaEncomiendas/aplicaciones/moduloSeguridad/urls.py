from django.urls import path
from . import views

app_name = 'seguridad_app'
urlpatterns = [
    path('Prueba/', views.Prueba,name='inicio_sesion'),
    path('crud/', views.crud,name='CRUD'),
    path('registro/', views.registro,name='registro'),

]
