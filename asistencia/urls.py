from django.urls import path
from .views import (
    GrupoListView, GrupoCreateView, AsistenteListView, AsistenteCreateView,
    AsistenciaCreateView, ReunionCreateView, dashboard_grupo, dashboard_asistente,
    filter_asistentes, search_asistentes
)

urlpatterns = [
    path('grupos/', GrupoListView.as_view(), name='grupo_list'),
    path('grupos/nuevo/', GrupoCreateView.as_view(), name='grupo_create'),
    path('asistentes/', AsistenteListView.as_view(), name='asistente_list'),
    path('asistentes/nuevo/', AsistenteCreateView.as_view(), name='asistente_create'),
    path('asistencias/nuevo/', AsistenciaCreateView.as_view(), name='asistencia_create'),
    path('reuniones/nuevo/', ReunionCreateView.as_view(), name='reunion_create'),
    path('filter-asistentes/', filter_asistentes, name='filter_asistentes'),
    path('search-asistentes/', search_asistentes, name='search_asistentes'),  # Nueva URL
    path('dashboard/grupo/<int:grupo_id>/', dashboard_grupo, name='dashboard_grupo'),
    path('dashboard/asistente/<int:asistente_id>/', dashboard_asistente, name='dashboard_asistente'),
]