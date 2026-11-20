from django.db import models
from registro.models import Perfil
from catalogo.models import Actividad

# Create your models here.
class Carrito(models.Model):
    usuario = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def total(self):
        total = 0
        for i in self.items.all():
            total += i.sub_total()
        return total

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def sub_total(self):
        return self.cantidad * self.actividad.precio

class Inscripcion(models.Model):
    turista = models.ForeignKey(Perfil, on_delete=models.CASCADE)  
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE) 
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='Pendiente')

class Pago(models.Model):
    inscripcion = models.OneToOneField(Inscripcion, on_delete=models.CASCADE) 
    monto = models.PositiveIntegerField()
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='Pendiente')
    codigo_transaccion = models.CharField(max_length=60, blank=True)
