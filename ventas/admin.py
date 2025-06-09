from django.contrib import admin
from .models import Pedido, DetallePedido, Historial


admin.site.register(Historial)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'estado', 'total']
    filter_horizontal = ['libros']  # Widget para seleccionar libros desde el admin
