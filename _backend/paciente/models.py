from django.db import models
from paciente.helpers.checar_cpf_valido import checar_cpf_valido
from paciente.helpers.checar_nome_valido import checar_nome_valido
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    cpf = models.CharField(max_length=14)

    aftas = models.BooleanField(default=False)
    hipersensibilidade = models.BooleanField(default=False)
    lesoes = models.BooleanField(default=False)
    pos_cirurgia = models.BooleanField(default=False)
    nevralgia = models.BooleanField(default=False)
    consulta = models.BooleanField(default=False)

    @property
    def nome(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def prontuario(self):
        doencas = []
        if self.aftas:
            doencas.append('aftas')
        if self.consulta:
            doencas.append('consultas')
        if self.hipersensibilidade:
            doencas.append('hipersensibilidade')
        if self.lesoes:
            doencas.append('lesoes')
        if self.nevralgia:
            doencas.append('nevralgias')
        if self.pos_cirurgia:
            doencas.append('pos_cirurgias')
        return doencas
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def clean(self):
        checar_nome_valido(self.nome)
        checar_cpf_valido(self.cpf)

        if Paciente.objects.exclude(pk=self.pk).filter(cpf=self.cpf).exists():
            raise ValidationError('Já existe um cadastro com este CPF.')

    def full_clean(self, *args, **kwargs):
        # Modify the fields before validation
        self.nome = self.nome.strip()
        self.cpf = self.cpf.replace('-', '').replace('.', '').strip()

        super(Paciente, self).full_clean(*args, **kwargs) # chama full_clean antes de chamar clean