from django.db import models

class OfertaLaboral(models.Model):
    cargo = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    salario = models.CharField(max_length=100, blank=True, null=True)
    tipo_contrato = models.CharField(max_length=100, blank=True, null=True)
    fecha_publicacion = models.DateField(blank=True, null=True)
    fuente = models.CharField(max_length=100)
    url = models.URLField(max_length=500)

    def __str__(self):
        return f"{self.cargo} en {self.empresa}"
