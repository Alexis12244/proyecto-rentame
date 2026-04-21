from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):

    class Meta:
        model = Comentario

        fields = [
            'calificacion',
            'comentario'
        ]

        widgets = {

            'calificacion': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'comentario': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Escribe tu comentario...'
                }
            ),
        }