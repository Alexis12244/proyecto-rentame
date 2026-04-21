from django.shortcuts import render

def lista_blog(request):
    return render(request, 'blog/lista.html')

def detalle_blog(request, id):
    return render(request, 'blog/detalle.html')

def contacto(request):
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        return render(request, 'blog/contacto.html', {'enviado': True})

    return render(request, 'blog/contacto.html')