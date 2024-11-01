from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Ruta
from .forms import RutaForm
from ..moduloUsuarios.models import Repartidor
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
# Create your views here.

class ListarRuta(ListView):
    model = Ruta
    template_name = 'moduloEntRec/listarRutas.html'
    context_object_name = 'ruta'
class CrearRuta(CreateView):
    model = Ruta
    form_class = RutaForm
    template_name = 'moduloEntRec/crearRuta.html'
    success_url = reverse_lazy('moduloEntRec:ListarRutas')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['repartidor'].queryset = Repartidor.objects.all() 
        return form
    
class EditarRuta(UpdateView):
    model = Ruta
    form_class = RutaForm
    template_name = 'moduloEntRec/editarRuta.html'
    success_url = reverse_lazy('moduloEntRec:ListarRutas')


class EliminarRuta(DeleteView):
    model = Ruta
    template_name = "moduloEntRec/listarRuta.html"
    success_url = reverse_lazy('moduloEntRec:ListarRutas')

    def delete(self, request, *args, **kwargs):
        ruta = self.get_object()
        try:
            ruta.delete()
            messages.success(request, 'Ruta eliminada correctamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar la ruta: {str(e)}')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Ruta eliminada correctamente!'})
        
        return super().delete(request, *args, **kwargs)
