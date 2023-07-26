from django.contrib import admin
from medico.models import Medico

# Register your models here.

from .models import Medico

class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'especialidades', 'dias_de_trabalho_str') # Elementos a serem mostrados na lista
    list_display_links = ('nome_completo', 'especialidades') # Elementos que quando clicados levam a página de edição
    list_filter = ('aftas', 'consulta', 'hipersensibilidade', 'lesoes', 'nevralgia', 'pos_cirurgia',) # caixinha de filtro por elemento passado por parâmetro
    search_fields = ('nome', 'especialidades') # itens que podem ser pesquisados
    list_per_page = 25 # quantos elementos por página


admin.site.register(Medico, MedicoAdmin)