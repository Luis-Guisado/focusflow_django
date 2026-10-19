from django.shortcuts import render, redirect, get_object_or_404
from .models import Habito
from .forms import HabitoForm

# Create your views here.
def listar_habitos(request):
    habitos = Habito.objects.select_related("categoria").order_by("nombre")
    return render(request, "habitos/lista_habitos.html", {"habitos": habitos})

def crear_habito(request):
    form = HabitoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("habitos:listar_habitos")
    return render(request, "habitos/formulario_habito.html", {"form": form})

def editar_habito(request, pk):
    habito = get_object_or_404(Habito, pk=pk)
    form = HabitoForm(request.POST or None, instance=habito)
    if form.is_valid():
       form.save()
       return redirect("habitos:listar_habitos")
    return render(request, "habitos/formulario_habito.html", {"form": form})

def eliminar_habito(request, pk):
    habito = get_object_or_404(Habito, pk=pk)
    if request.method == "POST":
        habito.delete()
        return redirect("habitos:listar_habitos")
    return render(request, "habitos/confirmar_eliminar.html", {"habito": habito})