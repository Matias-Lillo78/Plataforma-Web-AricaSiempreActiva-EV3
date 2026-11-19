from django.contrib import admin
from .models import Rol, Perfil, Administrador

# Register your models here.
admin.site.register(Rol)
admin.site.register(Perfil)
admin.site.register(Administrador)
