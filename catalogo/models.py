from django.db import models
from gremios.models import Gremio

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    gremio = models.ForeignKey(Gremio, on_delete=models.CASCADE)  
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)  
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    fecha = models.DateField()
    precio = models.PositiveIntegerField(default=0)
    cupo_maximo = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=20, default='Activa')
    imagen = models.ImageField(upload_to='actividades', null=True, blank=True)

    def __str__(self):
        return self.titulo
