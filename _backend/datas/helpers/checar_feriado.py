import holidays
from django.core.exceptions import ValidationError

def checar_feriado(data, dia, mes):
    feriados = holidays.Brazil()

    if data in feriados:
        raise ValidationError('Esse dia é feriado!')
    else:
        if (dia == 24 and mes == 6) or (dia == 29 and mes == 6) or (dia == 16 and mes == 9) or (dia == 20 and mes == 11) or (dia == 30 and mes == 11) or (dia == 27 and mes == 8) or (dia == 8 and mes == 12) or (dia == 6 and mes == 29) or (dia == 11 and mes == 20):
            raise ValidationError('Esse dia é feriado!')
