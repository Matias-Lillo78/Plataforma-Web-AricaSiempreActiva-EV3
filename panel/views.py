from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg
from registro.models import Administrador
from gremios.models import Gremio, Certificacion, HistorialDecision
from catalogo.models import Categoria, Actividad
from catalogo.forms import CategoriaForm
from carrito.models import Inscripcion, Pago
from experiencias.models import Comentario

def _admin_del_usuario(request):
    return get_object_or_404(Administrador, perfil__usuario=request.user)

@login_required
def panel_inicio(request):
    _admin_del_usuario(request)
    return render(request, 'panel/panel.html', {
        'pendientes': Certificacion.objects.filter(estado_solicitud='Pendiente'),
        'gremios': Gremio.objects.all(),
        'categorias': Categoria.objects.annotate(total=Count('actividad')),  
        'historial': HistorialDecision.objects.order_by('-id')[:10],
        'form': CategoriaForm(),
    })

@login_required
def revisar_certificacion(request, id):
    _admin_del_usuario(request)
    certificacion = get_object_or_404(Certificacion, pk=id)
    return render(request, 'panel/revisar.html', {
        'c': certificacion,
        'historial': certificacion.historialdecision_set.order_by('-id'),
    })

@login_required
def decidir_certificacion(request, id):
    admin = _admin_del_usuario(request)
    certificacion = get_object_or_404(Certificacion, pk=id)
    estado = request.POST.get('estado')    
    mensaje = request.POST.get('mensaje', '')

    if request.method == 'POST' and estado in ['Aprobada', 'Rechazada', 'Observada']:
        if estado != 'Aprobada' and not mensaje:
            messages.error(request, 'Escribe un mensaje para el gremio')
            return redirect('revisar-certificacion', id)

        HistorialDecision.objects.create(
            administrador=admin,
            certificacion=certificacion,
            estado_anterior=certificacion.estado_solicitud,
            estado_nuevo=estado,
            observaciones=mensaje,
        )
        certificacion.estado_solicitud = estado
        certificacion.mensaje_admin = mensaje
        certificacion.administrador = admin
        if estado == 'Aprobada':
            certificacion.fecha_emision = date.today()
            certificacion.estado_vigencia = 'Vigente'
        certificacion.save()
        messages.success(request, f'Solicitud {estado.lower()}')
    return redirect('panel')

@login_required
def crear_categoria(request):
    _admin_del_usuario(request)
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Categoría creada')
    return redirect('panel')

@login_required
def eliminar_categoria(request, id):
    _admin_del_usuario(request)
    categoria = get_object_or_404(Categoria, pk=id)

    if request.method == 'POST':
        if categoria.actividad_set.exists() or categoria.experienciapanorama_set.exists():
            messages.error(request, f'No se puede eliminar "{categoria}": tiene actividades asociadas')
        else:
            categoria.delete()
            messages.success(request, 'Categoría eliminada')
    return redirect('panel')

@login_required
def estadisticas(request):
    _admin_del_usuario(request)

    
    solicitudes = []
    for estado in ['Pendiente', 'Observada', 'Aprobada', 'Rechazada']:
        solicitudes.append((estado, Certificacion.objects.filter(estado_solicitud=estado).count()))

    return render(request, 'panel/estadisticas.html', {
        'total_gremios': Gremio.objects.count(),
        'verificados': Gremio.objects.filter(certificacion__estado_solicitud='Aprobada').distinct().count(),
        'total_actividades': Actividad.objects.count(),
        'personas': Inscripcion.objects.aggregate(Sum('cantidad'))['cantidad__sum'] or 0,
        'ingresos': Pago.objects.aggregate(Sum('monto'))['monto__sum'] or 0,
        'promedio': Comentario.objects.aggregate(Avg('valoracion'))['valoracion__avg'],
        'solicitudes': solicitudes,
        'total_solicitudes': Certificacion.objects.count(),
        'categorias': Categoria.objects.annotate(total=Count('actividad')).order_by('-total'),
        'top': Actividad.objects.annotate(personas=Sum('inscripcion__cantidad')).filter(personas__gt=0).order_by('-personas')[:5],
    })
