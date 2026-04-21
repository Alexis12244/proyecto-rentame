from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Publicacion

def lista_publicaciones(request):
    publicaciones = Publicacion.objects.all()
    return render(request, 'comunidad/lista.html', {'publicaciones': publicaciones})


@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        imagen = request.FILES.get('imagen')
        comentario = request.POST.get('comentario')

        Publicacion.objects.create(
            usuario=request.user,
            imagen=imagen,
            comentario=comentario
        )

        return redirect('comunidad')

    return render(request, 'comunidad/crear.html')