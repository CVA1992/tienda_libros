from django.db import models
from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)  # Relación con Autor
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='libros/', blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.autor})"

class Reseña(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='reseñas')
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)  # User por defecto
    comentario = models.TextField()
    puntuacion = models.PositiveIntegerField(choices=[(1, '★'), (2, '★★'), (3, '★★★'), (4, '★★★★'), (5, '★★★★★')])
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña de {self.usuario} para {self.libro}"