from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from django.shortcuts import render

from cabanas import views as cabanas_views
from cabanas.models import Cabana, Comentario
from reservas import views as reservas_views
from blog import views as blog_views
from comunidad import views as comunidad_views
def home(request):

    # 🏡 Cabañas recientes
    cabanas_recientes = Cabana.objects.all().order_by('-id')[:3]

    # ⭐ Mejor calificadas
    cabanas = Cabana.objects.all()

    cabanas_mejores = sorted(
        cabanas,
        key=lambda c: c.promedio_calificacion(),
        reverse=True
    )[:3]

    # 💬 Comentarios recientes
    comentarios_recientes = Comentario.objects.all().order_by('-fecha')[:4]

    return render(
        request,
        'home.html',
        {
            'cabanas_recientes': cabanas_recientes,
            'cabanas_mejores': cabanas_mejores,
            'comentarios_recientes': comentarios_recientes
        }
    )
urlpatterns = [

    path('', home, name='home'),
    # ADMIN
    path('admin/', admin.site.urls),

    # ========================
    # 🏡 CABAÑAS (CATÁLOGO)
    # ========================
    path('lista-cabanas/', cabanas_views.lista_cabanas, name='lista_cabanas'),
    path('cabana/<int:id>/', cabanas_views.detalle_cabana, name='detalle_cabana'),

    # ========================
    # 📅 RESERVAS
    # ========================
    path('reservar/<int:id>/', reservas_views.reservar, name='reservar'),
    path('mis-reservas/', reservas_views.mis_reservas, name='mis_reservas'),
    path('cancelar-reserva/<int:id>/', reservas_views.cancelar_reserva, name='cancelar_reserva'),

    # ========================
    # 📰 BLOG / PROMOCIONES
    # ========================
    path('blog/', blog_views.lista_blog, name='lista_blog'),
    path('blog/<int:id>/', blog_views.detalle_blog, name='detalle_blog'),

    # ========================
    # 👥 COMUNIDAD
    # ========================
    path('comunidad/', comunidad_views.lista_publicaciones, name='comunidad'),
    path('comunidad/crear/', comunidad_views.crear_publicacion, name='crear_publicacion'),

    # ========================
    # 📩 CONTACTO
    # ========================
    path('contacto/', blog_views.contacto, name='contacto'),

    # ========================
    # 🔐 USUARIOS
    # ========================
    path('usuarios/', include('usuarios.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)