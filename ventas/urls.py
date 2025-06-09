from django.urls import path
from . import views

urlpatterns = [
    path('lista_pedidos/',views.lista_pedidos, name="lista_pedidos"),
    path('detalle_pedido/<int:pedido_id>/',views.detalle_pedido,name="detalle_pedido"),
]