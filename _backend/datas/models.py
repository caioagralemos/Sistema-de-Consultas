from django.db import models
from datetime import datetime
from datas.helpers.disponibilidade_data import disponibilidade_data
from django.core.exceptions import ValidationError

# Create your models here.

def validar_ano(ano):
        if ano < datetime.now().year:
            raise ValidationError('Ano inválido!')

def validar_mes(ano, mes):
    if ano == datetime.now().year and mes < datetime.now().month:
            raise ValidationError('Mes inválido. Esse mes já passou.')
    elif mes < 1 or mes > 12:
            raise ValidationError('Mes inválido.')

def validar_dia(ano, mes, dia):
        if dia > 31 or dia < 1:
            raise ValidationError('Dia inválido.')
    
        if ano == datetime.now().year and mes == datetime.now().month and dia < datetime.now().day:
            raise ValidationError('Dia inválido. Esse dia já passou.')
        
        if mes == 2:
            if ano % 4 == 0:
                if dia <= 29:
                    pass
                else:
                    raise ValidationError('Dia inválido. Fevereiro tem 29 dias.')
            else:
                if dia <= 28:
                    pass
                else:
                    raise ValidationError('Dia inválido. Fevereiro tem 28 dias.')

        elif mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
            if dia <= 31:
                pass
            else:
                raise ValidationError('Dia inválido. Esse mes tem 31 dias.')

        elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
            if dia <= 30:
                pass
            else:
                raise ValidationError('Dia inválido. Esse mes tem 30 dias.')


class Data(models.Model):
    dia = models.IntegerField()
    mes = models.IntegerField()
    ano = models.IntegerField()

    def __str__(self):
        return f'{self.dia}/{self.mes}/{self.ano}'
    
    def clean(self): # o mêtodo clean faz todas as verificações
        validar_ano(self.ano)
        validar_mes(self.ano, self.mes)
        validar_dia(self.ano, self.mes, self.dia)
        disponibilidade_data(self.ano, self.mes, self.dia)