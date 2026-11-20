from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_inicio, name='panel'),
    path('certificacion/<int:id>/<str:estado>/', views.decidir_certificacion, name='decidir-certificacion'),
    path('categoria/crear/', views.crear_categoria, name='crear-categoria'),
]
