from django.shortcuts import render, get_object_or_404, redirect
from .models import Libro, Reseña
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import random
from django.core.paginator import Paginator
from django.db.models import Count
from .forms import ReseñaForm
from django.contrib import messages
from django.db import transaction
import logging




logger = logging.getLogger(__name__)

def detalle_libro(request, libro_id):
    # Obtener el libro y reseñas existentes
    libro = get_object_or_404(Libro, pk=libro_id)
    reseñas = libro.reseñas.all().order_by('-fecha')
    
    # Debug: Verificar acceso
    logger.debug(f"Accediendo a libro ID: {libro_id}, usuario: {request.user.username if request.user.is_authenticated else 'Anónimo'}")

    # Manejar edición (GET)
    reseña_editando = None
    if 'editar_reseña' in request.GET and request.user.is_authenticated:
        reseña_id = request.GET.get('editar_reseña')
        try:
            reseña_editando = get_object_or_404(Reseña, pk=reseña_id, usuario=request.user)
            logger.debug(f"Iniciando edición de reseña ID: {reseña_id}")
        except Exception as e:
            logger.error(f"Error al editar reseña: {str(e)}")
            messages.error(request, 'No puedes editar esta reseña')

    # Manejar todas las operaciones POST
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para realizar esta acción')
            return redirect('login') + f'?next={request.path}'

        # Añadir nueva reseña
        if 'añadir_reseña' in request.POST:
            form = ReseñaForm(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        reseña = form.save(commit=False)
                        reseña.libro = libro
                        reseña.usuario = request.user
                        reseña.save()
                        logger.info(f"Reseña añadida - ID: {reseña.id}, Usuario: {request.user.username}")
                        messages.success(request, '✅ Reseña añadida correctamente')
                except Exception as e:
                    logger.error(f"Error al guardar reseña: {str(e)}")
                    messages.error(request, '❌ Error al guardar la reseña')
            else:
                logger.warning(f"Formulario inválido: {form.errors}")
                messages.error(request, '❌ Corrige los errores en el formulario')
            return redirect('libros:detalle_libro', libro_id=libro.id)

        # Editar reseña existente
        elif 'editar_reseña' in request.POST:
            reseña_id = request.POST.get('reseña_id')
            try:
                reseña = get_object_or_404(Reseña, pk=reseña_id, usuario=request.user)
                form = ReseñaForm(request.POST, instance=reseña)
                if form.is_valid():
                    form.save()
                    logger.info(f"Reseña editada - ID: {reseña_id}")
                    messages.success(request, '✅ Reseña actualizada correctamente')
                else:
                    logger.warning(f"Errores al editar: {form.errors}")
                    messages.error(request, '❌ Error al actualizar la reseña')
            except Exception as e:
                logger.error(f"Error al editar reseña: {str(e)}")
                messages.error(request, '❌ No tienes permiso para editar esta reseña')
            return redirect('libros:detalle_libro', libro_id=libro.id)

        # Eliminar reseña
        elif 'eliminar_reseña' in request.POST:
            reseña_id = request.POST.get('reseña_id')
            try:
                reseña = get_object_or_404(Reseña, pk=reseña_id, usuario=request.user)
                reseña.delete()
                logger.info(f"Reseña eliminada - ID: {reseña_id}")
                messages.success(request, '✅ Reseña eliminada correctamente')
            except Exception as e:
                logger.error(f"Error al eliminar reseña: {str(e)}")
                messages.error(request, '❌ No puedes eliminar esta reseña')
            return redirect('libros:detalle_libro', libro_id=libro.id)

    # Contexto para el template
    context = {
        'libro': libro,
        'reseñas': reseñas,
        'form': ReseñaForm(),
        'reseña_editando': reseña_editando,
        'reseña_form': ReseñaForm(),  # Para opciones de puntuación
    }
    
    return render(request, 'libros/detalle.html', context)



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





def lista_categorias(request):
    # Obtener categorías distintas con conteo de libros
    categorias = Libro.objects.values('categoria').annotate(
        total=Count('id')
    ).order_by('categoria')
    
    return render(request, 'libros/lista_categorias.html', {
        'categorias': categorias
    })


def por_categoria(request, categoria):
    libros = Libro.objects.filter(categoria__iexact=categoria.replace('-', ' ')).order_by('titulo')
    return render(request, 'libros/lista_libros_categoria.html', {
        'categoria_actual': categoria.replace('-', ' '),
        'libros': libros
    })
