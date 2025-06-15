from django.shortcuts import render, get_object_or_404, redirect
from .models import Libro, Reseña
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import random
from django.core.paginator import Paginator
from django.db.models import Count

def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    reseñas = libro.reseñas.all()
    return render(request, 'libros/detalle.html', {'libro': libro, 'reseñas': reseñas})
def inicio(request):
    


    libros_filtrados = Libro.objects.filter(stock__lt=8).order_by('stock')[:8]

    libros = Libro.objects.all()
    libro = random.choice(libros) if libros else None
    return render(request, 'libros/inicio.html', { 'libro': libro, 'libros_filtrados':libros_filtrados})



def lista_libros(request):
    libros_list = Libro.objects.all()  # O tu queryset actual
    paginator = Paginator(libros_list, 9)  # Muestra 9 libros por página
    page_number = request.GET.get('page')
    libros = paginator.get_page(page_number)
    
    return render(request, 'libros/lista.html', {'libros': libros})


def buscar_libros(request):
    query = request.GET.get('q', '')  # Obtiene el parámetro de búsqueda (ej: ?q=harry+potter)
    
    if query:
        # Búsqueda en título, autor o descripción (no sensible a mayúsculas)
        libros = Libro.objects.filter(
            Q(titulo__icontains=query) | 
            Q(autor__nombre__icontains=query) |
            Q(descripcion__icontains=query)
        ).distinct()
    else:
        libros = Libro.objects.none()  # Si no hay query, devuelve lista vacía
    
    return render(request, 'libros/resultados_busqueda.html', {
        'libros': libros,
        'query': query
    })


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


def lista_categorias(request):
    # Obtener categorías distintas con conteo de libros
    categorias = Libro.objects.values('categoria').annotate(
        total=Count('id')
    ).order_by('categoria')
    
    return render(request, 'libros/lista_categorias.html', {
        'categorias': categorias
    })

# views.py
def por_categoria(request, categoria):
    libros = Libro.objects.filter(categoria__iexact=categoria.replace('-', ' ')).order_by('titulo')
    return render(request, 'libros/lista_libros_categoria.html', {
        'categoria_actual': categoria.replace('-', ' '),
        'libros': libros
    })