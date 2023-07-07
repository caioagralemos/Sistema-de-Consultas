def disponibilidade_data(consulta, objeto):
    for c in objeto:
        if consulta.data.dia == c['data']['dia'] and consulta.data.mes == c['data']['mes'] and consulta.data.ano == c['data']['ano']:
            return False
    
    else:
        return True
