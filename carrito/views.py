import random
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalogo.models import Actividad
from .models import Carrito, ItemCarrito, Inscripcion, Pago

def _carrito_del_usuario(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user.perfil)
    return carrito

def _item_del_usuario(request, item_id):
    return get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user.perfil)

@login_required
def ver_carrito(request):
    carrito = _carrito_del_usuario(request)
    return render(request, 'carrito/ver_carrito.html', {
        'items': carrito.items.all(),
        'total': carrito.total(),
    })

@login_required
def mis_inscripciones(request):
    
    inscripciones = Inscripcion.objects.filter(turista=request.user.perfil).order_by('-id')
    total = 0
    for i in inscripciones:
        total += i.pago.monto
    return render(request, 'carrito/mis_inscripciones.html', {
        'inscripciones': inscripciones,
        'total': total,
        'hoy': date.today(),
    })

@login_required
def agregar_carrito(request, id):
    if request.user.perfil.rol.nombre != 'Turista':
        return redirect('lista-actividades')

    actividad = get_object_or_404(Actividad, pk=id)
    if actividad.cupo_maximo <= 0:
        messages.error(request, 'No hay cupos')
        return redirect('lista-actividades')

    carrito = _carrito_del_usuario(request)
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, actividad=actividad)

    if not creado:
        if item.cantidad < actividad.cupo_maximo:
            item.cantidad += 1
            item.save()
        else:
            messages.error(request, 'No quedan cupos')

    return redirect('ver-carrito')

@login_required
def incrementar_item(request, id):
    item = _item_del_usuario(request, id)
    if item.cantidad < item.actividad.cupo_maximo:
        item.cantidad += 1
        item.save()
    return redirect('ver-carrito')

@login_required
def disminuir_item(request, id):
    item = _item_del_usuario(request, id)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    return redirect('ver-carrito')

@login_required
def eliminar_item(request, id):
    item = _item_del_usuario(request, id)
    item.delete()
    return redirect('ver-carrito')

@login_required
def pagar(request):
    carrito = _carrito_del_usuario(request)
    items = list(carrito.items.all())
    if not items:
        return redirect('ver-carrito')
    total = carrito.total()

    if request.method == 'POST':
        resultado = request.POST.get('resultado')  

        if resultado == 'Rechazado':
            
            return render(request, 'carrito/resultado_pago.html', {'aprobado': False, 'total': total})

        
        for item in items:
            if item.cantidad > item.actividad.cupo_maximo:
                messages.error(request, f'No quedan cupos suficientes en {item.actividad}')
                return redirect('ver-carrito')

        codigo = f'TRX-{random.randint(100000, 999999)}'  
        for item in items:
            inscripcion = Inscripcion.objects.create(
                turista=request.user.perfil,
                actividad=item.actividad,
                cantidad=item.cantidad,
                estado='Confirmada',
            )
            Pago.objects.create(inscripcion=inscripcion, monto=item.sub_total(), estado='Aprobado', codigo_transaccion=codigo)
            item.actividad.cupo_maximo -= item.cantidad 
            item.actividad.save()

        carrito.items.all().delete()  
        return render(request, 'carrito/resultado_pago.html', {
            'aprobado': True, 'items': items, 'total': total, 'codigo': codigo,
        })

    return render(request, 'carrito/pagar.html', {'items': items, 'total': total})
