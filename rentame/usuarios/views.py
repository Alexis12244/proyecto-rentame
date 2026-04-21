from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import RegistroForm


# REGISTRO
def registro(request):

    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('lista_cabanas')

    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {
        'form': form
    })


# LOGIN
def iniciar_sesion(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('lista_cabanas')

    else:
        form = AuthenticationForm()

    return render(request, 'usuarios/login.html', {
        'form': form
    })


# LOGOUT
def cerrar_sesion(request):
    logout(request)
    return redirect('lista_cabanas')
