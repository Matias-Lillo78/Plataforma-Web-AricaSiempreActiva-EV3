from django import forms
from .models import Actividad, Categoria

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['titulo', 'descripcion', 'categoria', 'fecha', 'precio', 'cupo_maximo', 'imagen']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
