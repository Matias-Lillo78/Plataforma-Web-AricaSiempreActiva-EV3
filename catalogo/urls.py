from django.urls import path
from . import views

urlpatterns = [
    path("", views.ActividadListView, name='listar_actividad'),
    path("crear/", views.ActividadCreateView, name='crear_actividad'),
    path("actualizar/<int:id>/", views.ActividadUpdateView, name='actualizar_actividad'),
]
