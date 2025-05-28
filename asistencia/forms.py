from django import forms
from .models import Asistente, Reunion, Asistencia

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['asistente', 'reunion', 'estado', 'notas']