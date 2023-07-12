from datetime import datetime, timedelta

def disponibilidade_data(consulta, objeto):
    data = datetime(consulta.data.ano, consulta.data.mes, consulta.data.dia)
    umano = datetime.now() + timedelta(days=365)

    if data > umano: # se for mais de um ano na frente
        return 'Uma das consultas está mais de 1 ano na frente da data de hoje.'
    
    if data.weekday() == 6: # se for num domingo
        return 'Uma das consultas cairia num domingo.'
    
    for c in objeto: # se tiver alguma consulta no dia
        if consulta.data.dia == c['data']['dia'] and consulta.data.mes == c['data']['mes'] and consulta.data.ano == c['data']['ano']:
            return f'Já existem consultas marcadas para o dia {consulta.data.dia}/{consulta.data.mes}/{consulta.data.ano}'
    
    return 'ok'
