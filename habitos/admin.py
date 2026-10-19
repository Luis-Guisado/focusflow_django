from django.contrib import admin
from .models import Categoria, Habito, RegistroHabito

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    
@admin.register(Habito)
class HabitoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "frecuencia", "meta_semanal", "activo")
    list_filter = ("categoria", "frecuencia", "activo")
    search_fields = ("nombre",)
    
@admin.register(RegistroHabito)
class RegistroHabitoAdmin(admin.ModelAdmin):
    list_display = ("habito", "fecha", "completado")
    list_filter = ("completado", "fecha")