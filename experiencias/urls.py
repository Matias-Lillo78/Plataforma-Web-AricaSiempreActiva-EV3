from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.lista_experiencias, name='lista-experiencias'),
    path('<int:id>/', views.detalle_experiencia, name='detalle-experiencia'),
    path('<int:id>/comentar/', views.comentar_experiencia, name='comentar-experiencia'),
    path('mis-experiencias/', views.mis_experiencias, name='mis-experiencias'),
]
