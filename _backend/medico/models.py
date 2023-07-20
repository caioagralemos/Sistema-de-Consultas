from django.db import models
from medico.helpers.checar_cpf_valido import checar_cpf_valido
from medico.helpers.checar_nome_valido import checar_nome_valido

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

    trabalha_segunda = models.BooleanField(default=True) # 0
    trabalha_terca = models.BooleanField(default=True) # 1
    trabalha_quarta = models.BooleanField(default=True) # 2
    trabalha_quinta = models.BooleanField(default=True) # 3
    trabalha_sexta = models.BooleanField(default=True) # 4
    trabalha_sabado = models.BooleanField(default=False) # 5

    @property
    def especialidades(self):
        esp = []
        if self.trabalha_com_aftas:
            esp.append('aftas')
        if self.trabalha_com_consulta:
            esp.append('consultas')
        if self.trabalha_com_hipersensibilidade:
            esp.append('hipersensibilidade')
        if self.trabalha_com_lesoes:
            esp.append('lesoes')
        if self.trabalha_com_nevralgia:
            esp.append('nevralgias')
        if self.trabalha_com_pos_cirurgia:
            esp.append('pos-cirurgias')
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
        return self.nome
    
    def clean(self):
        checar_cpf_valido(self.cpf)

    def full_clean(self, *args, **kwargs):
        # Modify the fields before validation
        self.nome = self.nome.strip()
        self.cpf = self.cpf.replace('-', '').replace('.', '').strip()

        super(Medico, self).full_clean(*args, **kwargs) # chama full_clean antes de chamar clean