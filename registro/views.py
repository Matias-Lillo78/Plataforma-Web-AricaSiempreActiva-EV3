from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import TuristaForm, GremioForm
from gremios.models import Gremio
from .models import Perfil, Rol, Administrador

# Create your views here.
def registrarView(request):
    tipo = request.POST.get('tipo', 'turista')
    datos = request.POST or None
    turista_form = TuristaForm(datos if tipo == 'turista' else None)
    gremio_form = GremioForm(datos if tipo == 'gremio' else None, prefix='gremio')
    form = gremio_form if tipo == 'gremio' else turista_form

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        rol, _ = Rol.objects.get_or_create(nombre=tipo.capitalize())  # 'Turista' o 'Gremio'
        perfil = Perfil.objects.create(usuario=user, rol=rol)
        if tipo == 'gremio':
            Gremio.objects.create(
                perfil=perfil,
                nombre_empresa=form.cleaned_data['nombre_empresa'],
                contacto=form.cleaned_data['contacto'],
                direccion=form.cleaned_data['direccion'],
                sitio_web=form.cleaned_data['sitio_web'],
            )
        messages.success(request, 'Usuario creado')
        return redirect('login')

    return render(request, 'registro/registro.html', {
        'turista_form': turista_form,
        'gremio_form': gremio_form,
        'tipo': tipo,
    })

def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            perfil, _ = Perfil.objects.get_or_create(usuario=user)
            if user.is_superuser:
                perfil.rol, _ = Rol.objects.get_or_create(nombre='Administrador')
                perfil.save()
                Administrador.objects.get_or_create(perfil=perfil, defaults={'nivel_acceso': 'Total'})
            login(request, user)
            return redirect('home')
        messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()
    return render(request, 'registro/login.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('home')
