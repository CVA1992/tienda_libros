from django.contrib import admin
from .models import Pedido, DetallePedido, Historial

admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Historial)