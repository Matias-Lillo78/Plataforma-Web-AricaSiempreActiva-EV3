from django.db import models

# Create your models here.
class Suscriptor(models.Model):
    correo = models.EmailField('Correo', unique=True)
    fecha = models.DateTimeField('Fecha de suscripción', auto_now_add=True)

    def __str__(self):
        return self.correo