from django import forms
from .models import Actividad, Categoria

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['titulo', 'descripcion', 'categorias', 'fecha', 'precio', 'cupo_maximo', 'imagen'] 
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        help_texts = {
            'categorias': 'Mantén presionada la tecla Ctrl para elegir más de una.',
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
