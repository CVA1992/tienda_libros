from django.urls import path
from . import views

urlpatterns = [
    path('libro/<int:libro_id>/', views.detalle_libro, name='detalle_libro'),
    path('libro/<int:libro_id>/reseña/', views.agregar_reseña, name='agregar_reseña'),
]