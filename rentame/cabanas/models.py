from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Cabana(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    costo_por_noche = models.DecimalField(max_digits=8, decimal_places=2)
    capacidad = models.IntegerField()
    servicios = models.TextField()
    imagen = models.ImageField(upload_to='cabanas/', null=True, blank=True)

    class Meta:
        verbose_name = 'Cabaña'
        verbose_name_plural = 'Cabañas'

    def __str__(self):
        return self.nombre
    
    # ⭐ PROMEDIO DE CALIFICACIÓN
    def promedio_calificacion(self):

        promedio = self.comentarios.aggregate(
            Avg('calificacion')
        )['calificacion__avg']

        return round(promedio, 1) if promedio else 0

class ImagenCabana(models.Model):

    cabana = models.ForeignKey(
        Cabana,
        on_delete=models.CASCADE,
        related_name='imagenes'
    )

    imagen = models.ImageField(
        upload_to='cabanas/'
    )

    def __str__(self):
        return f"Imagen de {self.cabana.nombre}"  

class Comentario(models.Model):

    cabana = models.ForeignKey(
        Cabana,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    calificacion = models.IntegerField(
        choices=[
            (1, '⭐'),
            (2, '⭐⭐'),
            (3, '⭐⭐⭐'),
            (4, '⭐⭐⭐⭐'),
            (5, '⭐⭐⭐⭐⭐'),
        ]
    )

    comentario = models.TextField()

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.cabana.nombre}"