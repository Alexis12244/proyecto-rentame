from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Cabana, Comentario
from .forms import ComentarioForm
from django.contrib.auth.decorators import login_required


def lista_cabanas(request):
    cabanas = Cabana.objects.all()
    return render(request, 'cabanas/lista.html', {'cabanas': cabanas})


def detalle_cabana(request, id):

    cabana = get_object_or_404(Cabana, id=id)

    comentarios = cabana.comentarios.all().order_by('-fecha')

    promedio = cabana.promedio_calificacion()

    if request.method == 'POST':

        if request.user.is_authenticated:

            form = ComentarioForm(request.POST)

            if form.is_valid():

                nuevo = form.save(commit=False)

                nuevo.usuario = request.user
                nuevo.cabana = cabana

                nuevo.save()

                return redirect('detalle_cabana', id=id)

        else:

            return redirect('/usuarios/login/')

    else:

        form = ComentarioForm()

    return render(
        request,
        'cabanas/detalle.html',
        {
            'cabana': cabana,
            'comentarios': comentarios,
            'form': form,
            'promedio': promedio
        }
    )

