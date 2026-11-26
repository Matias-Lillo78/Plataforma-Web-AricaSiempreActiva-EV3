from django.urls import path
from . import views

urlpatterns = [
    path('solicitar-certificacion/', views.solicitar_certificacion, name='solicitar-certificacion'),
    path('documento/<int:id>/eliminar/', views.eliminar_documento, name='eliminar-documento'),
    path('estadisticas/', views.estadisticas_gremio, name='estadisticas-gremio'),
]
