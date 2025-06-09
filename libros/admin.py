from django.contrib import admin

from .models import Autor, Libro, Reseña

admin.site.register(Autor)

admin.site.register(Reseña)


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'precio']  # Configuración específica para Libro