import random
from django.core.management.base import BaseCommand
from libros.models import Libro

class Command(BaseCommand):
    help = 'Actualiza el stock de libros vacío o nulo con valores aleatorios entre 1 y 20'

    def handle(self, *args, **options):
        # Obtener libros con stock None o 0 (según tu default=0)
        libros = Libro.objects.filter(stock__isnull=True) | Libro.objects.filter(stock=0)
        
        count = 0
        for libro in libros:
            libro.stock = random.randint(1, 20)
            libro.save()
            count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Se actualizó el stock de {count} libros con valores entre 1-20')
        )