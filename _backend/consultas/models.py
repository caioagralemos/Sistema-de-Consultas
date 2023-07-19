from django.db import models
from data.models import Data

# Create your models here.

class Consulta(models.Model):
    nome = models.CharField(max_length=70)
    cpf = models.CharField(max_length=14)
    data = models.ForeignKey(Data, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.dia}/{self.mes}/{self.ano}'