from django.urls import path
from . import views
app_name='ventas'
urlpatterns = [
    path('lista_pedidos/',views.lista_pedidos, name="lista_pedidos"),
    path('detalle_pedido/<int:pedido_id>/',views.detalle_pedido,name="detalle_pedido"),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:libro_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('actualizar/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('proceder_pago/',views.proceder_pago,name='proceder_pago'),
]