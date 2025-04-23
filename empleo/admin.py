from django.contrib import admin
from .models import OfertaLaboral

@admin.register(OfertaLaboral)
class OfertaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'empresa', 'ciudad', 'salario', 'tipo_contrato', 'fecha_publicacion', 'fuente')
    search_fields = ('cargo', 'empresa', 'ciudad')
