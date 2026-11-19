from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import PerfilForm
from .models import Perfil
from django.contrib.auth import login, logout
from django.contrib import messages

# Create your views here.
def registrarView(request):
    
    form = PerfilForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado')
            return redirect('')

    return render(request, 'registro/registro.html', {'form':form})


def loginView(request):
    if request.user.is_authenticated:
        return redirect ('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            perfil,_=Perfil.objects.get_or_create(user=user)
            login(request, user)
            return redirect('')
        
    else:
        form = AuthenticationForm()
    return render(request, 'registro/login.html', {'form':form})
    

def cerrar_sesion(request):
    logout(request)
    return redirect('home')

