from django.contrib import admin
from .models import Gremio, Certificacion, HistorialDecision

# Register your models here.
admin.site.register(Gremio)
admin.site.register(HistorialDecision)


class CertificacionAdmin(admin.ModelAdmin):
    list_display = ['gremio', 'fecha_solicitud', 'estado_solicitud']
    list_editable = ['estado_solicitud']

admin.site.register(Certificacion, CertificacionAdmin)
