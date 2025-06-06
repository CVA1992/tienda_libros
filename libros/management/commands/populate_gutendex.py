import requests
from django.core.management.base import BaseCommand
from libros.models import Libro, Autor

class Command(BaseCommand):
    help = 'Importa libros desde la API de Gutendex'

    def handle(self, *args, **kwargs):
        # Paso 1: Hacer petición a la API
        url = "https://gutendex.com/books/?languages=es"  # Libros en español
        response = requests.get(url)
        data = response.json()

        # Paso 2: Procesar cada libro
        for book in data['results']:
            # Extraer datos del libro
            title = book.get('title', 'Título desconocido')
            authors = book.get('authors', [])
            download_count = book.get('download_count', 0)
            
            # Paso 3: Manejar autores (puede haber múltiples)
            autor_nombre = authors[0]['name'] if authors else 'Anónimo'
            autor, _ = Autor.objects.get_or_create(nombre=autor_nombre)

            # Paso 4: Crear el libro en tu BD
            Libro.objects.create(
                titulo=title,
                autor=autor,
                precio=9.99,  # Precio por defecto
                descripcion=f"Descargas: {download_count}",
                imagen=book.get('formats', {}).get('image/jpeg', '')
            )

        self.stdout.write(self.style.SUCCESS(f'¡Se importaron {len(data["results"])} libros!'))