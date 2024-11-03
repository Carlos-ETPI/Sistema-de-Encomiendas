from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Ruta
from .forms import RutaForm
from ..moduloUsuarios.models import Repartidor
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,UpdateView,DeleteView,DetailView
from ..moduloUsuarios.views import group_required
from django.utils.decorators import method_decorator
# Create your views here.
@method_decorator(group_required('Jefe'), name='dispatch')
class ListarRuta(ListView):
    model = Ruta
    template_name = 'moduloEntRec/listarRutas.html'
    context_object_name = 'rutas'
@method_decorator(group_required('Jefe'), name='dispatch')
class CrearRuta(CreateView):
    model = Ruta
    form_class = RutaForm
    template_name = 'moduloEntRec/crearRuta.html'
    success_url = reverse_lazy('moduloEntRec:ListarRutas')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['id_repartidor'].queryset = Repartidor.objects.all() 
        return form
@method_decorator(group_required('Jefe'), name='dispatch')
class EditarRuta(UpdateView):
    model = Ruta
    form_class = RutaForm
    template_name = 'moduloEntRec/editarRuta.html'
    success_url = reverse_lazy('moduloEntRec:ListarRutas')
    
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['id_repartidor'].queryset = Repartidor.objects.all() 
        return form

@method_decorator(group_required('Jefe'), name='dispatch')
class VerRuta(DetailView):
    model=Ruta
    template_name='moduloEntRec/verRuta.html'
    context_object_name='rutas'
    
group_required('Jefe')
def EliminarRuta(request, pk):
    ruta = get_object_or_404(Ruta, pk=pk)

    if request.method == "POST":
        try:
            ruta.delete()
            # Agregar mensaje de éxito
            messages.success(request, 'Ruta eliminada correctamente!')
        except Exception as e:
            # Agregar mensaje de error si ocurre una excepción
            messages.error(request, f'Error al eliminar la ruta: {str(e)}')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Ruta eliminada correctamente!'})
        return redirect("moduloEntRec:ListarRutas")

    return render(request, "moduloEntRec/eliminarRuta.html", {"ruta": ruta})

