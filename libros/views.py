from django.shortcuts import render, get_object_or_404, redirect
from .models import Libro, Reseña
from django.contrib.auth.decorators import login_required

def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    reseñas = libro.reseñas.all()  # Obtiene todas las reseñas del libro
    return render(request, 'libros/detalle.html', {'libro': libro, 'reseñas': reseñas})


def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'libros/lista.html', {'libros': libros})

@login_required
def agregar_reseña(request, libro_id):
    if request.method == 'POST':
        libro = get_object_or_404(Libro, pk=libro_id)
        comentario = request.POST.get('comentario')
        puntuacion = request.POST.get('puntuacion')
        Reseña.objects.create(
            libro=libro,
            usuario=request.user,
            comentario=comentario,
            puntuacion=puntuacion
        )
        return redirect('detalle_libro', libro_id=libro.id)
    return redirect('inicio')