from django.db import models
from datas.models import Data
from medico.models import Medico
from paciente.models import Paciente

# Create your models here.

class Consulta(models.Model):
    OPCAO_1 = 'consulta'
    OPCAO_2 = 'aftas'
    OPCAO_3 = 'hipersensibilidade'
    OPCAO_4 = 'pos_cirurgia'
    OPCAO_5 = 'lesoes'
    OPCAO_6 = 'nevralgia'

    OPCOES_CHOICES = [
        (OPCAO_1, 'Consulta'),
        (OPCAO_2, 'Aftas'),
        (OPCAO_3, 'Hipersensibilidade'),
        (OPCAO_4, 'Pós-cirurgia'),
        (OPCAO_5, 'Lesões'),
        (OPCAO_6, 'Nevralgia'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.DO_NOTHING, related_name='consultas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='consultas')
    data = models.ForeignKey(Data, on_delete=models.DO_NOTHING)
    servico = models.CharField(
        choices=OPCOES_CHOICES,
        default=OPCAO_1,  # Valor padrão
    )
    ehParte2 = models.BooleanField(default=False)

    @property
    def data_hora_completa(self):
        return [self.data.ano, self.data.mes, self.data.dia, self.data.hora, self.data.minuto]
    
    class Meta:
        ordering = ['data__ano', 'data__mes', 'data__dia', 'data__hora', 'data__minuto']
