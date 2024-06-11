from django.urls import path
from . import views

urlpatterns = [
    path('Prueba/', views.Prueba),
    path('crud/', views.crud),
]
