from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pedido, Carrito, ItemCarrito
from libros.models import Libro
import random

def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request,'ventas/lista_pedidos.html', {'pedidos': pedidos})
def detalle_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    libros = pedido.libros.all()  # Obtiene todos los libros del pedido
    
    return render(request, 'ventas/detalle_pedido.html', {
        'pedido': pedido,
        'libros': libros,
    })
@login_required
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