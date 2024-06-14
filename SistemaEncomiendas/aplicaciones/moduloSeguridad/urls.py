from django.urls import path
from . import views

app_name = 'seguridad_app'
urlpatterns = [
    path('login/', views.LoginUser.as_view(),name='inicio_sesion'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('crud/', views.crud,name='CRUD'),
    path('registro/', views.registro,name='registro'),

]
