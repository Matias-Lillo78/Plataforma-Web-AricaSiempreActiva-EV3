from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from registro.models import Perfil
from gremios.models import Gremio
from .models import ExperienciaPanorama, Valoracion
from .forms import ComentarioForm, ValoracionForm


def lista_experiencias(request):
    experiencias = ExperienciaPanorama.objects.all()
    return render(request, 'experiencias/experiencia_list.html', {'experiencias': experiencias})

def detalle_experiencia(request, id):
    experiencia = get_object_or_404(ExperienciaPanorama, pk=id)
    return render(request, 'experiencias/experiencia_detail.html', {
        'experiencia': experiencia,
        'comentarios': experiencia.comentario_set.order_by('-id'),
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



@login_required
def mis_experiencias(request):

    gremio = get_object_or_404(Gremio, perfil__usuario=request.user)
    experiencias = ExperienciaPanorama.objects.filter(gremio=gremio)
    return render(request, 'experiencias/mis_experiencias.html', {'experiencias': experiencias})
