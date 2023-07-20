from django.contrib import admin
from paciente.models import Paciente

# Register your models here.

from .models import Paciente

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'prontuario') # Elementos a serem mostrados na lista
    list_display_links = ('nome',  'cpf') # Elementos que quando clicados levam a página de edição
    search_fields = ('nome', 'cpf') # itens que podem ser pesquisados
    list_per_page = 25 # quantos elementos por página

admin.site.register(Paciente, PacienteAdmin)