from django import forms
from .models import Asistente, Reunion, Asistencia, GrupoTrabajo

class AsistenciaForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(queryset=GrupoTrabajo.objects.all(), required=True, label="Seleccionar Grupo")

    class Meta:
        model = Asistencia
        fields = ['asistente', 'reunion', 'estado', 'notas']

    def clean(self):
        cleaned_data = super().clean()
        grupo = cleaned_data.get('grupo')
        asistente = cleaned_data.get('asistente')
        if grupo and asistente and asistente not in grupo.asistentes.all():
            raise forms.ValidationError("El asistente seleccionado no pertenece al grupo elegido.")
        return cleaned_data