from datetime import datetime, timedelta
from components.helpers.checar_feriado import checar_feriado

def disponibilidade_data(ano, mes, dia, objeto):
    data = datetime(ano, mes, dia)
    umano = datetime.now() + timedelta(days=365)

    if checar_feriado(data, dia, mes): # se o dia for feriado
        return f'Uma das consultas caiu num feriado.\nConsulta do dia {dia}/{mes}/{ano}'

    if data > umano: # se for mais de um ano na frente
        return f'Uma das consultas está mais de 1 ano na frente da data de hoje.\nConsulta do dia {dia}/{mes}/{ano}'
    
    if data.weekday() == 6: # se for num domingo
        return f'Uma das consultas cairia num domingo.\nConsulta do dia {dia}/{mes}/{ano}'
    
    for c in objeto: # se tiver alguma consulta no dia
        if dia == c['data']['dia'] and mes == c['data']['mes'] and ano == c['data']['ano']:
            return f'Já existem consultas marcadas para o dia {dia}/{mes}/{ano}'
    
    return 'ok'
