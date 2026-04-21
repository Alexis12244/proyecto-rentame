from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Reserva
from cabanas.models import Cabana
from datetime import datetime
from django.shortcuts import get_object_or_404

from django.db.models import Q

@login_required
def reservar(request, id):
    cabana = Cabana.objects.get(id=id)

    # 🔥 Obtener fechas ocupadas
    reservas = Reserva.objects.filter(cabana=cabana)
    fechas_ocupadas = []

    for r in reservas:
        fechas_ocupadas.append({
            "start": str(r.fecha_entrada),
            "end": str(r.fecha_salida)
        })

    if request.method == 'POST':
        fecha_entrada = request.POST.get('fecha_entrada')
        fecha_salida = request.POST.get('fecha_salida')

        # Validar que existan
        if not fecha_entrada or not fecha_salida:
            return render(request, 'reservas/reservar.html', {
                'cabana': cabana,
                'error': 'Debes seleccionar ambas fechas',
                'fechas_ocupadas': fechas_ocupadas
            })

        # Convertir fechas
        f1 = datetime.strptime(fecha_entrada, "%Y-%m-%d")
        f2 = datetime.strptime(fecha_salida, "%Y-%m-%d")

        # Validar orden de fechas
        if f2 <= f1:
            return render(request, 'reservas/reservar.html', {
                'cabana': cabana,
                'error': 'La fecha de salida debe ser mayor que la de entrada',
                'fechas_ocupadas': fechas_ocupadas
            })

        #  VALIDAR QUE NO SE TOPEN FECHAS
        conflicto = Reserva.objects.filter(
            cabana=cabana
        ).filter(
            Q(fecha_entrada__lt=fecha_salida) &
            Q(fecha_salida__gt=fecha_entrada)
        )

        if conflicto.exists():
            return render(request, 'reservas/reservar.html', {
                'cabana': cabana,
                'error': 'Estas fechas ya están ocupadas',
                'fechas_ocupadas': fechas_ocupadas
            })

        # Calcular días y total
        dias = (f2 - f1).days
        total = dias * cabana.costo_por_noche

        # Guardar reserva
        Reserva.objects.create(
            usuario=request.user,
            cabana=cabana,
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            total=total
        )

        return redirect('mis_reservas')

    # GET
    return render(request, 'reservas/reservar.html', {
        'cabana': cabana,
        'fechas_ocupadas': fechas_ocupadas
    })


@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha_entrada')
    return render(request, 'reservas/mis_reservas.html', {'reservas': reservas})

@login_required
def cancelar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id, usuario=request.user)
    reserva.delete()
    return redirect('mis_reservas')