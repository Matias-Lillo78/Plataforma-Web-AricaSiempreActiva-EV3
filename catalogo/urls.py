from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_actividades, name='lista-actividades'),
    path('detalle/<int:id>/', views.detalle_actividad, name='detalle-actividad'),
    path('mis-actividades/', views.mis_actividades, name='mis-actividades'),
    path('crear/', views.crear_actividad, name='crear-actividad'),
    path('editar/<int:id>/', views.editar_actividad, name='editar-actividad'),
    path('eliminar/<int:id>/', views.eliminar_actividad, name='eliminar-actividad'),
]
