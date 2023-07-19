from django.db import models
from django.core.validators import RegexValidator
from datas.models import Data
from consultas.helpers.checar_cpf_valido import checar_cpf_valido
from consultas.helpers.checar_nome_valido import checar_nome_valido

# Create your models here.

class Consulta(models.Model):
    nome = models.CharField(max_length=70)
    cpf = models.CharField(max_length=14)
    data = models.ForeignKey(Data, on_delete=models.DO_NOTHING)
    
    def clean(self):
        checar_nome_valido(self.nome)
        checar_cpf_valido(self.cpf)

    def full_clean(self, *args, **kwargs):
        # Modify the fields before validation
        self.nome = self.nome.strip()
        self.cpf = self.cpf.replace('-', '').replace('.', '').strip()

        super(Consulta, self).full_clean(*args, **kwargs) # chama full_clean antes de chamar clean