from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TuristaForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.help_text = ''


class GremioForm(TuristaForm):
    nombre_empresa = forms.CharField(max_length=100)
    contacto = forms.CharField(max_length=100, required=False)
    direccion = forms.CharField(max_length=150, required=False)
    sitio_web = forms.CharField(max_length=150, required=False)

    class Meta(TuristaForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']
