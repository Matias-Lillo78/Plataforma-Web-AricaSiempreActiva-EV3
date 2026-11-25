from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Cuéntanos tu experiencia'}),
        }

class ValoracionForm(forms.Form):
    puntuacion = forms.IntegerField(min_value=1, max_value=5, label='Tu valoración (1 a 5)')