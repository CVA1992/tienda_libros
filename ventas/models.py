from django.db import models
from django.contrib.auth.models import User
from libros.models import Libro

  
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)  
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)   
    cantidad = models.PositiveIntegerField(default=1)

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    creado_en = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    estado = models.CharField(max_length=20, default='pendiente')  # Ej: 'pendiente', 'completado', 'cancelado'
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total del pedido

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')  # Relación con Pedido
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)  # Ajusta 'app_libros' según tu app
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=6, decimal_places=2)  # Precio en el momento de la compra

    def __str__(self):
        return f"{self.cantidad}x {self.libro.titulo} (Pedido #{self.pedido.id})"