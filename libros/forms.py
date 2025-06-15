from django import forms
from .models import Reseña

class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['comentario', 'puntuacion']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu reseña aquí...',
                'rows': 4
            }),
            'puntuacion': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'comentario': 'Tu opinión',
            'puntuacion': 'Puntuación'
        }