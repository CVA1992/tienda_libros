"""
URL configuration for tienda_libros project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# mi_sitio_libros/urls.py (URLs principales del proyecto)
from django.contrib import admin
from django.urls import path, include
from libros.views import inicio
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('libros.urls')),          # Página de inicio (catálogo)
    path('usuarios/', include('usuarios.urls')),
    path('ventas/', include('ventas.urls')),
    path('',inicio, name='inicio'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
]