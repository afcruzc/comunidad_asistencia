from django.db import models
from django.contrib.auth.models import User

class GrupoTrabajo(models.Model):
    nombre = models.CharField(max_length=100)
    lider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='grupos_liderados')
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Asistente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    grupos = models.ManyToManyField(GrupoTrabajo, related_name='asistentes')

    def __str__(self):
        return self.nombre

class Reunion(models.Model):
    fecha = models.DateTimeField()
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"Reunión - {self.fecha.strftime('%Y-%m-%d %H:%M')}"

class Asistencia(models.Model):
    ESTADO_CHOICES = (
        ('ASISTIO', 'Asistió'),
        ('TARDE', 'Llegó tarde'),
        ('INASISTIO', 'Inasistió'),
    )
    asistente = models.ForeignKey(Asistente, on_delete=models.CASCADE, related_name='asistencias')
    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE, related_name='asistencias')  # Corrección aquí
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"{self.asistente.nombre} - {self.reunion} - {self.estado}"