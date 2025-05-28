from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import GrupoTrabajo, Asistente, Reunion, Asistencia
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .forms import AsistenciaForm
from django.utils import timezone

# Vista para listar grupos
class GrupoListView(LoginRequiredMixin, ListView):
    model = GrupoTrabajo
    template_name = 'asistencia/grupo_list.html'
    context_object_name = 'grupos'

# Vista para crear un grupo
class GrupoCreateView(LoginRequiredMixin, CreateView):
    model = GrupoTrabajo
    fields = ['nombre', 'lider', 'descripcion']
    template_name = 'asistencia/grupo_form.html'
    success_url = reverse_lazy('grupo_list')

# Vista para listar asistentes
class AsistenteListView(LoginRequiredMixin, ListView):
    model = Asistente
    template_name = 'asistencia/asistente_list.html'
    context_object_name = 'asistentes'

# Vista para crear un asistente
class AsistenteCreateView(LoginRequiredMixin, CreateView):
    model = Asistente
    fields = ['nombre', 'correo', 'grupos']
    template_name = 'asistencia/asistente_form.html'
    success_url = reverse_lazy('asistente_list')

# Vista para editar un asistente
class AsistenteUpdateView(LoginRequiredMixin, UpdateView):
    model = Asistente
    fields = ['nombre', 'correo', 'grupos']
    template_name = 'asistencia/asistente_form.html'
    success_url = reverse_lazy('asistente_list')

# Vista para registrar asistencia
class AsistenciaCreateView(LoginRequiredMixin, CreateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = 'asistencia/asistencia_form.html'
    success_url = reverse_lazy('grupo_list')

# Vista para filtrar asistentes por grupo
@login_required
def filter_asistentes(request):
    grupo_id = request.GET.get('grupo_id')
    asistentes = Asistente.objects.filter(grupos__id=grupo_id).distinct()
    return render(request, 'asistencia/asistentes_dropdown.html', {'asistentes': asistentes})

# Vista para buscar asistentes por nombre
@login_required
def search_asistentes(request):
    query = request.GET.get('query', '')
    if query:
        asistentes = Asistente.objects.filter(nombre__icontains=query).distinct()
    else:
        asistentes = Asistente.objects.none()
    return render(request, 'asistencia/asistentes_search_results.html', {'asistentes': asistentes})

# Vista para crear una reunión
class ReunionCreateView(LoginRequiredMixin, CreateView):
    model = Reunion
    fields = ['fecha', 'descripcion']
    template_name = 'asistencia/reunion_form.html'
    success_url = reverse_lazy('grupo_list')

# Dashboard por grupo
@login_required
def dashboard_grupo(request, grupo_id):
    grupo = GrupoTrabajo.objects.get(id=grupo_id)
    asistencias = Asistencia.objects.filter(asistente__grupos=grupo).values('estado').annotate(total=Count('estado'))
    labels = [item['estado'] for item in asistencias]
    data = [item['total'] for item in asistencias]
    print(f"Labels: {labels}, Data: {data}")  # Depuración
    return render(request, 'asistencia/dashboard_grupo.html', {
        'grupo': grupo,
        'asistencias': asistencias,
        'chart_labels': labels,
        'chart_data': data,
    })

# Dashboard por asistente
@login_required
def dashboard_asistente(request, asistente_id):
    asistente = Asistente.objects.get(id=asistente_id)
    asistencias = Asistencia.objects.filter(asistente=asistente).order_by('reunion__fecha')
    # Preparar datos para el gráfico (ejemplo: asistencias por fecha)
    labels = [a.reunion.fecha.strftime('%Y-%m-%d') for a in asistencias]
    data = [1 if a.estado == 'ASISTIO' else 0 for a in asistencias]  # 1 para asistió, 0 para no asistió
    return render(request, 'asistencia/dashboard_asistente.html', {
        'asistente': asistente,
        'asistencias': asistencias,
        'chart_labels': labels,
        'chart_data': data,
    })