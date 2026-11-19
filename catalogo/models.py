from django.db import models
from registro.models import Perfil
from gremios.models import Gremio

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

class ExperienciaPanorama(models.Model):
    gremio = models.ForeignKey(Gremio, on_delete=models.CASCADE)  
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT) 
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='experiencias', null=True, blank=True)
    datos_contacto = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    turista = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    experiencia = models.ForeignKey(ExperienciaPanorama, on_delete=models.CASCADE)  
    texto = models.CharField(max_length=255)
    fecha = models.DateField(auto_now_add=True)

class Valoracion(models.Model):
    turista = models.ForeignKey(Perfil, on_delete=models.CASCADE)  # otorga
    experiencia = models.ForeignKey(ExperienciaPanorama, on_delete=models.CASCADE)  
    puntuacion = models.PositiveSmallIntegerField()  # 1 a 5
    fecha = models.DateField(auto_now_add=True)
