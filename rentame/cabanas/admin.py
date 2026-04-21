from django.contrib import admin
from .models import Cabana, ImagenCabana


class ImagenCabanaInline(admin.TabularInline):
    model = ImagenCabana
    extra = 3


class CabanaAdmin(admin.ModelAdmin):
    inlines = [ImagenCabanaInline]


admin.site.register(Cabana, CabanaAdmin)