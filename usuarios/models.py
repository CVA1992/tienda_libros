from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    TIPO_USUARIO = [
        ('C', 'Cliente'),
        ('A', 'Administrador'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo_usuario = models.CharField(max_length=1, choices=TIPO_USUARIO, default='C')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"Perfil de {self.usuario.username} - {self.get_tipo_usuario_display()}"