from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import PerfilUsuario

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear perfil asociado
            PerfilUsuario.objects.create(usuario=user)
            login(request, user)
            messages.success(request, "¡Registro exitoso!")
            return redirect('inicio')  # Cambia 'inicio' por tu vista principal
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})