from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Carrito, ItemCarrito, Pedido, DetallePedido
from libros.models import Libro
from usuarios.models import PerfilUsuario
import random
from decimal import Decimal
from django.db import transaction


def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request,'ventas/lista_pedidos.html', {'pedidos': pedidos})


@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.itemcarrito_set.all().select_related('libro')
    
    # Calcula subtotales y total
    for item in items:
        item.subtotal = item.libro.precio * item.cantidad
    
    total = sum(item.subtotal for item in items)
    
    context = {
        'carrito': carrito,
        'items': items,
        'total': total
    }
    return render(request, 'ventas/ver_carrito.html', context)

@login_required
def agregar_al_carrito(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    
    item, item_creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        libro=libro,
        defaults={'cantidad': 1}
    )
    
    if not item_creado:
        item.cantidad += 1
        item.save()
    
    messages.success(request, f'"{libro.titulo}" ha sido agregado al carrito')
    return redirect('ventas:ver_carrito')

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, 'Item eliminado del carrito')
    return redirect('ventas:ver_carrito')

@login_required
def actualizar_cantidad(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        
        if nueva_cantidad > 0:
            item.cantidad = nueva_cantidad
            item.save()
            messages.success(request, 'Cantidad actualizada')
        else:
            item.delete()
            messages.success(request, 'Item eliminado del carrito')
    
    return redirect('ventas:ver_carrito')
def proceder_pago(request):
    carrito=Carrito.objects.get(usuario=request.user)
    items_carrito = carrito.itemcarrito_set.all().select_related('libro')
    total = sum(item.libro.precio * item.cantidad for item in items_carrito)
    pedido = Pedido.objects.create(
        usuario=request.user,
        total=total,
        estado='pendiente'
    )
    for item in items_carrito:
        DetallePedido.objects.create(
            pedido=pedido,
            libro=item.libro,
            cantidad=item.cantidad,
            precio_unitario=item.libro.precio,
    )
    items_carrito.delete()
    messages.success(request, "¡Pedido añadido correctamente!")
    return redirect('inicio')
# views.py
from django.shortcuts import get_object_or_404

def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)  # Filtra por usuario para seguridad
    items_pedido = pedido.items.all().select_related('libro')  # Accede a los items mediante related_name
    return render(request, 'ventas/detalle_pedido.html', {'pedido': pedido, 'items_pedido':items_pedido})
@login_required
def historial(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request,'ventas/historial.html',{'pedidos':pedidos})