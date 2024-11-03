from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.generic import UpdateView,ListView,CreateView
from django.views.decorators.http import require_POST
from ..moduloUsuarios.views import group_required
from django.utils.decorators import method_decorator

#importacion de formularios
from .forms import pedidoForm, actualizarPedidoForm

# Importacion de modelos
from .models import Pedido

# Create your views here.
#---------------------------Gestion de pedidos----------------------------------
#vista para listas pedidos
@method_decorator(group_required('Jefe'), name='dispatch')
class crudPedido(ListView):
    model = Pedido
    template_name = "moduloOrdPaq/crudPedido.html"
    context_object_name = "lista_Pedidos"

    def get_queryset(self):
        #pedidos obtenidos del mas antiguo al mas reciente
        return Pedido.objects.order_by('fecha_creacion')

#Vista para crear pedido
@method_decorator(group_required('Jefe'), name='dispatch')
class crearPedido(CreateView):
    form_class = pedidoForm
    success_url = reverse_lazy('moduloOrdPaq:crudPedido')
    template_name = 'moduloOrdPaq/crearPedido.html'

    def form_valid(self, form):
        #form.instance.id_usuario = self.request.user
        return super().form_valid(form)
    
#vista para actulizar pedido
@method_decorator(group_required('Jefe'), name='dispatch')
class modificarPedido(UpdateView):
    model = Pedido
    template_name = 'moduloOrdPaq/modificarPedido.html'
    form_class = actualizarPedidoForm
    success_url = reverse_lazy("moduloOrdPaq:crudPedido")

    def form_valid(self, form):
        messages.success(self.request,"El pedido se ha actulizado de forma exitosa")
        return super().form_valid(form)
group_required('Jefe')
#vista para eliminar pedido
def eliminarPedido(request,pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == "POST":
        try:
            pedido.delete()
            #mensaje de eliminacion exitosa
            messages.success(request, 'El pedido fue removido de forma exitosa')
        except Exception as e:
            #mensaje de error
            messages.error(request, f'Error al eliminar el pedido: {str(e)}')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Pedido removido de forma exitosa!'})
        return redirect("moduloOrdPaq:crudPedido")
    return render(request, "moduloOrdPaq/eliminarPedido.html",{"pedido":pedido})

#vista para revisar datos del pedido realizado
group_required('Jefe')
def verPedido(request, pk):
    pedido = get_object_or_404(Pedido, id_pedido=pk)
    return render(request,'moduloOrdPaq/verPedido.html',{'pedido':pedido})