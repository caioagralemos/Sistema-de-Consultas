import holidays
from datetime import datetime
from django.core.exceptions import ValidationError

def checar_feriado(data):
    feriados = holidays.Brazil()

    if data in feriados:
        raise ValidationError('Esse dia é feriado!')
