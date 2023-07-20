from django.db import models
from consultas.helpers import checar_cpf_valido
from consultas.helpers import checar_nome_valido

# Create your models here.

class Medico(models.Model):
    nome = models.CharField(max_length=70)
    cpf = models.CharField(max_length=14)
    trabalha_com_aftas = models.BooleanField(default=False)
    trabalha_com_hipersensibilidade = models.BooleanField(default=False)
    trabalha_com_lesoes = models.BooleanField(default=False)
    trabalha_com_pos_cirurgia = models.BooleanField(default=False)
    trabalha_com_nevralgia = models.BooleanField(default=False)
    trabalha_com_consulta = models.BooleanField(default=False)

    def clean(self):
        checar_nome_valido(self.nome)
        checar_cpf_valido(self.cpf)

    def full_clean(self, *args, **kwargs):
        # Modify the fields before validation
        self.nome = self.nome.strip()
        self.cpf = self.cpf.replace('-', '').replace('.', '').strip()

        super(Medico, self).full_clean(*args, **kwargs) # chama full_clean antes de chamar clean