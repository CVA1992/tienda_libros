from django.contrib import admin
from .models import Pedido, DetallePedido





@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'estado', 'total']
    filter_horizontal = ['libros']  # Widget para seleccionar libros desde el admin
