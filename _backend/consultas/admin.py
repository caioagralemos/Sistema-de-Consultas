from django.contrib import admin
from .models import Consulta

# Register your models here.

from .models import Consulta

class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'data') # Elementos a serem mostrados na lista
    list_display_links = ('paciente',  'medico') # Elementos que quando clicados levam a página de edição
    search_fields = ('paciente',  'medico', 'data') # itens que podem ser pesquisados
    list_per_page = 25 # quantos elementos por página

admin.site.register(Consulta, ConsultaAdmin)