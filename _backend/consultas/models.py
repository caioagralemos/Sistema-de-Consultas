from django.db import models
from datas.models import Data
from medico.models import Medico
from paciente.models import Paciente

# Create your models here.

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.DO_NOTHING, related_name='consultas')
    medico = models.ForeignKey(Medico, on_delete=models.DO_NOTHING)
    data = models.ForeignKey(Data, on_delete=models.DO_NOTHING)