from django.urls import path
from . import views

urlpatterns = [
    path('solicitar-certificacion/', views.solicitar_certificacion, name='solicitar-certificacion'),
]
