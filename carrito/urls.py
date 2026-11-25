from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_carrito, name='ver-carrito'),
    path('agregar/<int:id>/', views.agregar_carrito, name='agregar-carrito'),
    path('incrementar/<int:id>/', views.incrementar_item, name='incrementar-carrito'),
    path('disminuir/<int:id>/', views.disminuir_item, name='disminuir-carrito'),
    path('eliminar/<int:id>/', views.eliminar_item, name='eliminar-carrito'),
    path('pagar/', views.pagar, name='pagar'),
    path('mis-inscripciones/', views.mis_inscripciones, name='mis-inscripciones'),
]
