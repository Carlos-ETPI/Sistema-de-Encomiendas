from django.shortcuts import render

# Create your views here.
def Prueba(request):
    return render(request,'moduloSeguridad/Prueba.html') 

def crud(request):
    return render(request,'moduloSeguridad/crud.html')