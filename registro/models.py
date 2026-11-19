from django.db import models
# importando user de django (Usuario del diagrama: nombre, email, contraseña y fecha de registro)
from django.contrib.auth.models import User

# funcion para rol por defecto
def rol_default():
    rol, _ = Rol.objects.get_or_create(nombre='Turista')
    return rol.id

class Rol(models.Model):
    # Roles: Turista, Gremio, Administrador
    nombre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.RESTRICT, default=rol_default)
    # usuario de django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    intentos_fallidos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.usuario.username} - {self.rol.nombre}"

class Administrador(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    nivel_acceso = models.CharField(max_length=20)

    def __str__(self):
        return self.perfil.usuario.username
