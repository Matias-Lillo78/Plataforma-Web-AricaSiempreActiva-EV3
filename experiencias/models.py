from django.db import models
from django.db.models import Avg
from registro.models import Perfil
from gremios.models import Gremio
from catalogo.models import Categoria, Actividad

# Create your models here.
class ExperienciaPanorama(models.Model):
    
    actividad = models.OneToOneField(Actividad, on_delete=models.CASCADE, null=True, blank=True)
    gremio = models.ForeignKey(Gremio, on_delete=models.CASCADE)  
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)  
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='experiencias', null=True, blank=True)
    datos_contacto = models.CharField(max_length=100)

    def promedio(self):
        
        return self.valoracion_set.aggregate(Avg('puntuacion'))['puntuacion__avg']

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    turista = models.ForeignKey(Perfil, on_delete=models.CASCADE) 
    experiencia = models.ForeignKey(ExperienciaPanorama, on_delete=models.CASCADE)  
    texto = models.CharField(max_length=255)
    fecha = models.DateField(auto_now_add=True)

class Valoracion(models.Model):
    turista = models.ForeignKey(Perfil, on_delete=models.CASCADE) 
    experiencia = models.ForeignKey(ExperienciaPanorama, on_delete=models.CASCADE)  
    puntuacion = models.PositiveSmallIntegerField()  
    fecha = models.DateField(auto_now_add=True)
