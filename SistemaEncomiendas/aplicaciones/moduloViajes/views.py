from django.shortcuts import render

# Create your views here.

#Vista para crear un nuevo viaje
def nuevoviaje(request):
    return render(request, 'moduloViajes/crearViaje.html')
def editarviaje(request):
    return render(request, 'moduloViajes/editarViaje.html')
def mostrarviajes(request):
    return render(request, 'moduloViajes/viajes.html')
