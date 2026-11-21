from django.db import models
from registro.models import Perfil, Administrador

# Create your models here.
class Gremio(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    nombre_empresa = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=150, blank=True)
    sitio_web = models.CharField(max_length=150, blank=True)

    def verificado(self):
        
        return self.certificacion_set.filter(estado_solicitud='Aprobada').exists()

    def __str__(self):
        return self.nombre_empresa

class Certificacion(models.Model):

    gremio = models.ForeignKey(Gremio, on_delete=models.CASCADE)  
    administrador = models.ForeignKey(Administrador, on_delete=models.SET_NULL, null=True, blank=True)  
    fecha_solicitud = models.DateField(auto_now_add=True)
    fecha_emision = models.DateField(null=True, blank=True)
    estado_solicitud = models.CharField(max_length=20, default='Pendiente')
    periodo_vigencia = models.PositiveIntegerField(default=12) 
    estado_vigencia = models.CharField(max_length=20, blank=True)
    antecedentes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.gremio} - {self.estado_solicitud}"

class HistorialDecision(models.Model):
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)  # decide
    # la decision puede ser sobre una certificacion o sobre una actividad
    certificacion = models.ForeignKey(Certificacion, on_delete=models.CASCADE, null=True, blank=True)
    actividad = models.ForeignKey('catalogo.Actividad', on_delete=models.CASCADE, null=True, blank=True)
    fecha_cambio = models.DateField(auto_now_add=True)
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    observaciones = models.CharField(max_length=255, blank=True)
