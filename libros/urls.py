from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Públicas
    path('lista_libros', views.lista_libros, name='lista_libros'),                  # Lista de libros (inicio)
    path('libro/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),  
    # Detalle de un libro,        # Búsqueda
    path('buscar/', views.buscar_libros, name='buscar_libros'),
    
    # Autenticadas
    path('reseña/agregar/<int:libro_id>/', views.agregar_reseña, name='agregar_reseña'),  # Solo usuarios logueados
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)