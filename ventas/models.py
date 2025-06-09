from django.db import models
from django.contrib.auth.models import User

from libros.models import Libro
from usuarios.models import PerfilUsuario

class Pedido(models.Model):
    ESTADOS = [
        ('P', 'Pendiente'),
        ('E', 'Enviado'),
        ('C', 'Cancelado'),
    ]
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    libros = models.ManyToManyField(Libro, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.libro.titulo}"

# Historial (puede ser una vista o un modelo separado)
class Historial(models.Model):
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha_consulta = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Historial"  # Para que no muestre "Historials" en el admin

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.libro.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad}x {self.libro.titulo} (${self.subtotal()})"