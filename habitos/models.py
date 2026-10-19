from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    
class Habito(models.Model):
    FRECUENCIAS = [
        ("diario", "Diario"),
        ("semanal", "Semanal"),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    frecuencia = models.CharField(max_length=10, choices=FRECUENCIAS, default="diario")
    meta_semanal = models.PositiveIntegerField(default=7)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    
class RegistroHabito(models.Model):
    habito = models.ForeignKey(Habito, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    completado = models.BooleanField(default=True)
    nota = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.habito.nombre} - {self.fecha}"