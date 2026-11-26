from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from catalogo.models import Actividad
from carrito.models import Inscripcion, Pago
from experiencias.models import Comentario
from .models import Gremio, Certificacion, Documento, validar_pdf

MAXIMO_DOCUMENTOS = 10


def _revisar_archivos(archivos, ya_subidos):
    total = ya_subidos + len(archivos)
    if total == 0:
        return 'Adjunta al menos un documento'
    if total > MAXIMO_DOCUMENTOS:
        return f'Puedes tener máximo {MAXIMO_DOCUMENTOS} documentos por solicitud'
    for archivo in archivos:
        try:
            validar_pdf(archivo)
        except forms.ValidationError as error:
            return f'{archivo.name}: {error.messages[0]}'
    return ''


@login_required
def solicitar_certificacion(request):
    gremio = get_object_or_404(Gremio, perfil__usuario=request.user)

    if gremio.certificacion_set.filter(estado_solicitud__in=['Pendiente', 'Aprobada']).exists():
        messages.error(request, 'Ya tienes una solicitud en revisión o aprobada')
        return redirect('mis-actividades')

    
    certificacion = gremio.certificacion_set.filter(estado_solicitud='Observada').first()

    if request.method == 'POST':
        archivos = request.FILES.getlist('documentos') 
        ya_subidos = certificacion.documentos.count() if certificacion else 0
        rut = request.POST.get('antecedentes', '').strip()
        error = _revisar_archivos(archivos, ya_subidos)
        if not rut:
            error = 'Escribe el RUT de la empresa'

        if error:
            messages.error(request, error)
        else:
            if certificacion is None:
                certificacion = Certificacion(gremio=gremio)
            certificacion.antecedentes = rut  
            certificacion.estado_solicitud = 'Pendiente'
            certificacion.save()
            for archivo in archivos:
                Documento.objects.create(certificacion=certificacion, nombre=archivo.name, archivo=archivo)
            messages.success(request, 'Solicitud enviada')
            return redirect('mis-actividades')

    return render(request, 'gremios/solicitud.html', {'certificacion': certificacion, 'maximo': MAXIMO_DOCUMENTOS})


@login_required
def eliminar_documento(request, id):
    
    documento = get_object_or_404(Documento, pk=id, certificacion__gremio__perfil__usuario=request.user,
                                  certificacion__estado_solicitud='Observada')
    if request.method == 'POST':
        documento.archivo.delete()  
        documento.delete()
        messages.success(request, 'Documento eliminado')
    return redirect('solicitar-certificacion')


@login_required
def estadisticas_gremio(request):
    gremio = get_object_or_404(Gremio, perfil__usuario=request.user)

    actividades = Actividad.objects.filter(gremio=gremio).annotate(
        personas=Sum('inscripcion__cantidad'),
        ingresos=Sum('inscripcion__pago__monto'),
    ).order_by('-personas')

    personas = Inscripcion.objects.filter(actividad__gremio=gremio).aggregate(Sum('cantidad'))['cantidad__sum'] or 0

    return render(request, 'gremios/estadisticas.html', {
        'gremio': gremio,
        'total_actividades': actividades.count(),
        'personas': personas,
        'ingresos': Pago.objects.filter(inscripcion__actividad__gremio=gremio).aggregate(Sum('monto'))['monto__sum'] or 0,
        'promedio': Comentario.objects.filter(experiencia__gremio=gremio).aggregate(Avg('valoracion'))['valoracion__avg'],
        'actividades': actividades,
    })
