from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from gremios.models import Gremio
from experiencias.models import ExperienciaPanorama
from .models import Actividad
from .forms import ActividadForm

def _gremio_del_usuario(request):
    return get_object_or_404(Gremio, perfil__usuario=request.user)

def _copiar_a_experiencia(actividad):
    ExperienciaPanorama.objects.update_or_create(
        actividad=actividad,
        defaults={
            'gremio': actividad.gremio,
            'categoria': actividad.categoria,
            'titulo': actividad.titulo,
            'descripcion': actividad.descripcion,
            'imagen': actividad.imagen,
            'datos_contacto': actividad.gremio.contacto,
        },
    )


def lista_actividades(request):
    actividades = Actividad.objects.filter(estado='Activa')
    return render(request, 'catalogo/actividad_list.html', {'actividades': actividades})

def detalle_actividad(request, id):
    actividad = get_object_or_404(Actividad, pk=id)
    return render(request, 'catalogo/actividad_detail.html', {'actividad': actividad})


@login_required
def mis_actividades(request):
    gremio = _gremio_del_usuario(request)
    actividades = Actividad.objects.filter(gremio=gremio)
    pendiente = gremio.certificacion_set.filter(estado_solicitud='Pendiente').exists()
    return render(request, 'catalogo/mis_actividades.html', {'actividades': actividades, 'gremio': gremio, 'pendiente': pendiente})

@login_required
def crear_actividad(request):
    gremio = _gremio_del_usuario(request)
    if not gremio.verificado():
        messages.error(request, 'Tu gremio debe estar verificado para publicar')
        return redirect('mis-actividades')

    form = ActividadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.gremio = gremio 
            actividad.save()
            _copiar_a_experiencia(actividad)  
            messages.success(request, 'Actividad creada')
            return redirect('mis-actividades')
        messages.error(request, 'La actividad no se pudo crear')
    return render(request, 'catalogo/actividad_form.html', {'form': form, 'accion': 'Crear'})

@login_required
def editar_actividad(request, id):

    actividad = get_object_or_404(Actividad, pk=id, gremio=_gremio_del_usuario(request))

    form = ActividadForm(request.POST or None, request.FILES or None, instance=actividad)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            _copiar_a_experiencia(actividad) 
            messages.success(request, 'Actividad actualizada')
            return redirect('mis-actividades')
    return render(request, 'catalogo/actividad_form.html', {'form': form, 'accion': 'Actualizar'})

@login_required
def eliminar_actividad(request, id):
    actividad = get_object_or_404(Actividad, pk=id, gremio=_gremio_del_usuario(request))

    if request.method == 'POST':
        actividad.delete() 
        messages.success(request, 'Actividad eliminada')
        return redirect('mis-actividades')
    return render(request, 'catalogo/actividad_delete.html', {'actividad': actividad})
