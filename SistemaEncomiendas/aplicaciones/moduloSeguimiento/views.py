from django.shortcuts import render
from django.contrib import messages
from django.views.generic import UpdateView,ListView,CreateView
from ..moduloOrdPaq.models import Pedido
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from ..moduloSeguimiento.forms import estadosForm
from django.urls import reverse_lazy
from ..moduloUsuarios .views import group_required
from django.utils.decorators import method_decorator
# Create your views here.
@method_decorator(group_required('Jefe'), name='dispatch')
class ListarEstados(ListView):
    model = Pedido
    template_name = "moduloSeguimiento/listarPedidoEstado.html"
    context_object_name = "lista_pedidos_estado"
    
    def get_queryset(self):
        estado = self.request.GET.get('estado')
        if estado and estado != "all":
            return Pedido.objects.filter(estado_pedido=estado)
        return Pedido.objects.all()
@group_required('Jefe')   
def prueba_vista(request):
    return render(request, 'moduloSeguimiento/modificarEstado.html', {})

@method_decorator(group_required('Jefe'), name='dispatch')
class CrearEstado(UpdateView):
    template_name = "moduloSeguimiento/modificarEstado.html"
    model = Pedido
    form_class = estadosForm
    success_url = reverse_lazy("moduloSeguimiento:cambiar_estado")

    def form_valid(self, form):
        # Guarda el formulario y actualiza el pedido
        response = super().form_valid(form)
        mensaje_usuario = self.request.POST.get("mensaje", "")
        # Datos para el correo
        pedido = self.object
        asunto = f"Pedido: {pedido.numero_orden}"
        mensaje = f"""
            Estado actual: {pedido.estado_pedido}
            Fecha de registro: {pedido.fecha_creacion.strftime('%d de %B de %Y a las %H:%M')}
            Descripción adicional: {mensaje_usuario}
        """
        mensaje_html = f"""
            <html>
                <body>
                    <div style="text-align: center;">
                        <img src="https://i.imgur.com/nBk4MAi.jpeg" alt="Imagen del pedido" width="200" height="200">
                        <h2>Pedido: {pedido.numero_orden}</h2>
                        <p>Estado actual: {pedido.estado_pedido}</p>
                        <p>Fecha de registro: {pedido.fecha_creacion.strftime('%d de %B de %Y a las %H:%M')}</p>
                        <p>Descripción adicional: {mensaje_usuario}</p>
                    </div>
                </body>
            </html>
        """
        destinatario = pedido.id_cliente.emailCliente  

        # Envío del correo
        try:
            send_mail(
                asunto,
                mensaje,
                settings.EMAIL_HOST_USER,
                [destinatario],
                fail_silently=False,
                html_message=mensaje_html,  
            )
            print("Correo enviado correctamente")  
        except Exception as e:
            print(f"Error al enviar el correo: {e}") 

        return response


