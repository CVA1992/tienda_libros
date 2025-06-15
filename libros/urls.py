from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'libros' 
urlpatterns = [
    # Públicas
    
    path('lista/', views.lista_libros, name='lista'),                  
    path('libro/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),  
    path('buscar/', views.buscar_libros, name='buscar_libros'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categoria/<str:categoria>/', views.por_categoria, name='por_categoria'),
   
     # Solo usuarios logueados
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)