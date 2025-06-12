import requests
from libros.models import Libro, Autor

def import_books(query="django"):
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

# Ejecutar:
# python manage.py shell < populate_books.py