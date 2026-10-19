from django import forms
from .models import Habito

class HabitoForm(forms.ModelForm):
    class Meta:
        model = Habito
        fields = ["nombre", "descripcion", "frecuencia", "meta_semanal", "categoria", "activo"]
        
    def clean_meta_semanal(self):
        meta = self.cleaned_data["meta_semanal"]
        if meta < 1 or meta > 7:
            raise forms.ValidationError("La meta semanal debe estar entre 1 y 7.")
        return meta