from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Gremio, Certificacion


@login_required
def solicitar_certificacion(request):
    gremio = get_object_or_404(Gremio, perfil__usuario=request.user)

    if request.method == 'POST':
        if gremio.certificacion_set.filter(estado_solicitud='Pendiente').exists():
            messages.error(request, 'Ya tienes una solicitud pendiente')
        else:
            Certificacion.objects.create(gremio=gremio, antecedentes=request.POST.get('antecedentes', ''))
            messages.success(request, 'Solicitud enviada')
    return redirect('mis-actividades')
