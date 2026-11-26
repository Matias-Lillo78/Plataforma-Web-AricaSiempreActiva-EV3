from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto', 'valoracion']
        labels = {
            'texto': 'Comentario',
            'valoracion': 'Valoración (1 a 5)',
        }
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Cuéntanos tu experiencia'}),
            'valoracion': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
