from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_inicio, name='panel'),
    path('certificacion/<int:id>/', views.revisar_certificacion, name='revisar-certificacion'),
    path('certificacion/<int:id>/decidir/', views.decidir_certificacion, name='decidir-certificacion'),
    path('categoria/crear/', views.crear_categoria, name='crear-categoria'),
    path('categoria/<int:id>/eliminar/', views.eliminar_categoria, name='eliminar-categoria'),
    path('estadisticas/', views.estadisticas, name='estadisticas-admin'),
]
