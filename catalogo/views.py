from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from registro.models import Perfil
from gremios.models import Gremio
from .models import Actividad, ExperienciaPanorama, Valoracion
from .forms import ActividadForm, ExperienciaForm, ComentarioForm, ValoracionForm


def _gremio_del_usuario(request):
    return get_object_or_404(Gremio, perfil__usuario=request.user)

################## CATALOGO ##################

def lista_actividades(request):
    actividades = Actividad.objects.filter(estado='Activa')
    return render(request, 'catalogo/actividad_list.html', {'actividades': actividades})

def detalle_actividad(request, id):
    actividad = get_object_or_404(Actividad, pk=id)
    return render(request, 'catalogo/actividad_detail.html', {'actividad': actividad})

################## CRUD DEL GREMIO ##################

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


def lista_experiencias(request):
    experiencias = ExperienciaPanorama.objects.all()
    return render(request, 'catalogo/experiencia_list.html', {'experiencias': experiencias})

def detalle_experiencia(request, id):
    experiencia = get_object_or_404(ExperienciaPanorama, pk=id)

    promedio = experiencia.valoracion_set.aggregate(Avg('puntuacion'))['puntuacion__avg']
    return render(request, 'catalogo/experiencia_detail.html', {
        'experiencia': experiencia,
        'comentarios': experiencia.comentario_set.order_by('-id'),
        'promedio': promedio,
        'comentario_form': ComentarioForm(),
        'valoracion_form': ValoracionForm(),
    })

@login_required
def comentar_experiencia(request, id):
    perfil = get_object_or_404(Perfil, usuario=request.user)
    experiencia = get_object_or_404(ExperienciaPanorama, pk=id)
    form = ComentarioForm(request.POST or None)

    if perfil.rol.nombre == 'Turista' and request.method == 'POST' and form.is_valid():
        comentario = form.save(commit=False)
        comentario.turista = perfil
        comentario.experiencia = experiencia
        comentario.save()
        messages.success(request, 'Comentario publicado')
    return redirect('detalle-experiencia', id=id)

@login_required
def valorar_experiencia(request, id):
    perfil = get_object_or_404(Perfil, usuario=request.user)
    experiencia = get_object_or_404(ExperienciaPanorama, pk=id)
    form = ValoracionForm(request.POST or None)

    if perfil.rol.nombre == 'Turista' and request.method == 'POST' and form.is_valid():

        Valoracion.objects.update_or_create(
            turista=perfil,
            experiencia=experiencia,
            defaults={'puntuacion': form.cleaned_data['puntuacion']},
        )
        messages.success(request, 'Gracias por tu valoración')
    return redirect('detalle-experiencia', id=id)

################## CRUD DE EXPERIENCIAS DEL GREMIO ##################

@login_required
def mis_experiencias(request):
    gremio = _gremio_del_usuario(request)
    experiencias = ExperienciaPanorama.objects.filter(gremio=gremio)
    return render(request, 'catalogo/mis_experiencias.html', {'experiencias': experiencias, 'gremio': gremio})

@login_required
def crear_experiencia(request):
    gremio = _gremio_del_usuario(request)
    if not gremio.verificado():
        messages.error(request, 'Tu gremio debe estar verificado para publicar')
        return redirect('mis-experiencias')

    form = ExperienciaForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.gremio = gremio  
            experiencia.save()
            messages.success(request, 'Experiencia publicada')
            return redirect('mis-experiencias')
        messages.error(request, 'La experiencia no se pudo publicar')
    return render(request, 'catalogo/experiencia_form.html', {'form': form, 'accion': 'Crear'})

@login_required
def editar_experiencia(request, id):
  
    experiencia = get_object_or_404(ExperienciaPanorama, pk=id, gremio=_gremio_del_usuario(request))

    form = ExperienciaForm(request.POST or None, request.FILES or None, instance=experiencia)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Experiencia actualizada')
            return redirect('mis-experiencias')
    return render(request, 'catalogo/experiencia_form.html', {'form': form, 'accion': 'Actualizar'})

@login_required
def eliminar_experiencia(request, id):
    experiencia = get_object_or_404(ExperienciaPanorama, pk=id, gremio=_gremio_del_usuario(request))

    if request.method == 'POST':
        experiencia.delete()
        messages.success(request, 'Experiencia eliminada')
        return redirect('mis-experiencias')
    return render(request, 'catalogo/experiencia_delete.html', {'experiencia': experiencia})
