from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from registro.models import Perfil
from gremios.models import Gremio
from carrito.models import Inscripcion
from .models import ExperienciaPanorama
from .forms import ComentarioForm


def lista_experiencias(request):
    
    if request.user.is_authenticated and hasattr(request.user, 'perfil'):
        if request.user.perfil.rol.nombre == 'Gremio':
            return redirect('mis-experiencias')
        if request.user.perfil.rol.nombre == 'Administrador':
            return redirect('panel')

    experiencias = ExperienciaPanorama.objects.all()
    return render(request, 'experiencias/experiencia_list.html', {'experiencias': experiencias})

def detalle_experiencia(request, id):
    experiencia = get_object_or_404(ExperienciaPanorama, pk=id)


    inscrito = False
    if request.user.is_authenticated:
        inscrito = Inscripcion.objects.filter(turista__usuario=request.user, actividad=experiencia.actividad).exists()

    return render(request, 'experiencias/experiencia_detail.html', {
        'experiencia': experiencia,
        'inscrito': inscrito,
        'comentarios': experiencia.comentario_set.order_by('-id'),
        'comentario_form': ComentarioForm(),
    })

@login_required
def comentar_experiencia(request, id):
    perfil = get_object_or_404(Perfil, usuario=request.user)
    experiencia = get_object_or_404(ExperienciaPanorama, pk=id)
    form = ComentarioForm(request.POST or None)
    inscrito = Inscripcion.objects.filter(turista=perfil, actividad=experiencia.actividad).exists()

    if inscrito and request.method == 'POST' and form.is_valid():
        comentario = form.save(commit=False)
        comentario.turista = perfil
        comentario.experiencia = experiencia
        comentario.save()
        messages.success(request, 'Comentario publicado')
    return redirect('detalle-experiencia', id=id)



@login_required
def mis_experiencias(request):

    gremio = get_object_or_404(Gremio, perfil__usuario=request.user)
    experiencias = ExperienciaPanorama.objects.filter(gremio=gremio)
    return render(request, 'experiencias/mis_experiencias.html', {'experiencias': experiencias})
