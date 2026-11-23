from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from registro.models import Administrador
from gremios.models import Gremio, Certificacion, HistorialDecision
from catalogo.models import Categoria
from catalogo.forms import CategoriaForm

# busca el administrador que inicio sesion (si no es administrador da 404)
def _admin_del_usuario(request):
    return get_object_or_404(Administrador, perfil__usuario=request.user)

@login_required
def panel_inicio(request):
    _admin_del_usuario(request)
    return render(request, 'panel/panel.html', {
        'pendientes': Certificacion.objects.filter(estado_solicitud='Pendiente'),
        'gremios': Gremio.objects.all(),
        'categorias': Categoria.objects.all(),
        'historial': HistorialDecision.objects.order_by('-id')[:10],
        'form': CategoriaForm(),
    })

@login_required
def decidir_certificacion(request, id, estado):
    admin = _admin_del_usuario(request)
    certificacion = get_object_or_404(Certificacion, pk=id)

    if request.method == 'POST' and estado in ['Aprobada', 'Rechazada']:
        # se guarda la decision en el historial
        HistorialDecision.objects.create(
            administrador=admin,
            certificacion=certificacion,
            estado_anterior=certificacion.estado_solicitud,
            estado_nuevo=estado,
        )
        certificacion.estado_solicitud = estado
        certificacion.administrador = admin
        if estado == 'Aprobada':
            certificacion.fecha_emision = date.today()
            certificacion.estado_vigencia = 'Vigente'
        certificacion.save()
        messages.success(request, f'Certificación {estado.lower()}')
    return redirect('panel')

@login_required
def crear_categoria(request):
    _admin_del_usuario(request)
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Categoría creada')
    return redirect('panel')
