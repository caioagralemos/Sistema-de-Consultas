from datetime import datetime, timedelta
from components.helpers.checar_feriado import checar_feriado

def disponibilidade_data(ano, mes, dia, objeto):
    data = datetime(ano, mes, dia)
    umano = datetime.now() + timedelta(days=365)

    if checar_feriado(data): # se o dia for feriado
        return 'Uma das consultas caiu num feriado.'

    if data > umano: # se for mais de um ano na frente
        return 'Uma das consultas está mais de 1 ano na frente da data de hoje.'
    
    if data.weekday() == 6: # se for num domingo
        return 'Uma das consultas cairia num domingo.'
    
    for c in objeto: # se tiver alguma consulta no dia
        if dia == c['data']['dia'] and mes == c['data']['mes'] and ano == c['data']['ano']:
            return f'Já existem consultas marcadas para o dia {dia}/{mes}/{ano}'
    
    return 'ok'
