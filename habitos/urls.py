from django.urls import path
from . import views

app_name = "habitos"

urlpatterns = [
    path("", views.listar_habitos, name="listar_habitos"),
    path("crear/", views.crear_habito, name="crear_habito"),
    path("editar/<int:pk>/", views.editar_habito, name="editar_habito"),
    path("eliminar/<int:pk>/", views.eliminar_habito, name="eliminar_habito"),
]