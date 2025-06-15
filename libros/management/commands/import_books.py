
from django.core.management.base import BaseCommand
from libros.models import Libro, Autor
import requests

class Command(BaseCommand):
    help = 'Importa libros desde la API de Google Books'

    def add_arguments(self, parser):
        parser.add_argument('--query', type=str, default='web', help='Término de búsqueda')

    def handle(self, *args, **options):
        query = options['query']
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
        response = requests.get(url)
        data = response.json()

        for item in data.get('items', [])[:10]:  # Limita a 10 libros
            book_info = item['volumeInfo']
            autor, _ = Autor.objects.get_or_create(nombre=book_info.get('authors', ['Desconocido'])[0])
            
            Libro.objects.create(
                titulo=book_info['title'],
                autor=autor,
                precio=19.99,
                categoria=book_info.get('categories', ['General'])[0],
                descripcion=book_info.get('description', 'Sin descripción'),
                imagen=book_info.get('imageLinks', {}).get('thumbnail', '')
            )
        self.stdout.write(self.style.SUCCESS('Libros importados correctamente'))