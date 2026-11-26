from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from gremios.models import Gremio
from experiencias.models import ExperienciaPanorama
from .models import Actividad
from .forms import ActividadForm

def _gremio_del_usuario(request):
    return get_object_or_404(Gremio, perfil__usuario=request.user)

def _copiar_a_experiencia(actividad):
    experiencia, _ = ExperienciaPanorama.objects.update_or_create(
        actividad=actividad,
        defaults={
            'gremio': actividad.gremio,
            'titulo': actividad.titulo,
            'descripcion': actividad.descripcion,
            'imagen': actividad.imagen,
            'datos_contacto': actividad.gremio.contacto,
        },
    )
    experiencia.categorias.set(actividad.categorias.all())  

def lista_actividades(request):
   
    if request.user.is_authenticated and hasattr(request.user, 'perfil'):
        if request.user.perfil.rol.nombre == 'Gremio':
            return redirect('mis-actividades')
        if request.user.perfil.rol.nombre == 'Administrador':
            return redirect('panel')

    actividades = Actividad.objects.filter(estado='Activa')
    return render(request, 'catalogo/actividad_list.html', {'actividades': actividades})

def detalle_actividad(request, id):
    actividad = get_object_or_404(Actividad, pk=id)
    return render(request, 'catalogo/actividad_detail.html', {'actividad': actividad})


@login_required
def mis_actividades(request):
    gremio = _gremio_del_usuario(request)
    actividades = Actividad.objects.filter(gremio=gremio).annotate(inscritos=Sum('inscripcion__cantidad'))
    certificacion = gremio.certificacion_set.last()  

    
    id = request.GET.get('actividad')
    if id:
        elegida = get_object_or_404(actividades, pk=id)  # solo actividades de este gremio
    else:
        elegida = actividades.first()

    participantes = []
    recaudado = 0
    if elegida:
        participantes = elegida.inscripcion_set.all().order_by('-id')
        for inscripcion in participantes:
            recaudado += inscripcion.pago.monto

    return render(request, 'catalogo/mis_actividades.html', {
        'actividades': actividades,
        'gremio': gremio,
        'certificacion': certificacion,
        'elegida': elegida,
        'participantes': participantes,
        'recaudado': recaudado,
    })

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
            actividad.categorias.set(form.cleaned_data['categorias'])
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
