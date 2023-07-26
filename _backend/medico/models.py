from django.db import models
from medico.helpers.checar_cpf_valido import checar_cpf_valido
from medico.helpers.checar_nome_valido import checar_nome_valido
from django.contrib.auth.models import User


# Create your models here.

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cpf = models.CharField(max_length=14)

    aftas = models.BooleanField(default=False)
    hipersensibilidade = models.BooleanField(default=False)
    lesoes = models.BooleanField(default=False)
    pos_cirurgia = models.BooleanField(default=False)
    nevralgia = models.BooleanField(default=False)
    consulta = models.BooleanField(default=False)

    trabalha_segunda = models.BooleanField(default=True) # 0
    trabalha_terca = models.BooleanField(default=True) # 1
    trabalha_quarta = models.BooleanField(default=True) # 2
    trabalha_quinta = models.BooleanField(default=True) # 3
    trabalha_sexta = models.BooleanField(default=True) # 4
    trabalha_sabado = models.BooleanField(default=False) # 5

    @property
    def nome_completo(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def especialidades(self):
        esp = []
        if self.aftas:
            esp.append('Aftas')
        if self.consulta:
            esp.append('Consultas')
        if self.hipersensibilidade:
            esp.append('Hipersensibilidade')
        if self.lesoes:
            esp.append('Lesões')
        if self.nevralgia:
            esp.append('Nevralgias')
        if self.pos_cirurgia:
            esp.append('Pós-Cirurgias')
        return esp
    
    @property
    def dias_de_trabalho_str(self):
        dias = []
        if self.trabalha_segunda:
            dias.append('Segunda')
        if self.trabalha_terca:
            dias.append('Terça')
        if self.trabalha_quarta:
            dias.append('Quarta')
        if self.trabalha_quinta:
            dias.append('Quinta')
        if self.trabalha_sexta:
            dias.append('Sexta')
        if self.trabalha_sabado:
            dias.append('Sábado')
        return dias

    @property
    def dias_de_trabalho(self):
        dias = []
        if self.trabalha_segunda:
            dias.append(0)
        if self.trabalha_terca:
            dias.append(1)
        if self.trabalha_quarta:
            dias.append(2)
        if self.trabalha_quinta:
            dias.append(3)
        if self.trabalha_sexta:
            dias.append(4)
        if self.trabalha_sabado:
            dias.append(5)
        return dias

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def clean(self):
        checar_cpf_valido(self.cpf)

    def full_clean(self, *args, **kwargs):
        self.cpf = self.cpf.replace('-', '').replace('.', '').strip()

        super(Medico, self).full_clean(*args, **kwargs) # chama full_clean antes de chamar clean