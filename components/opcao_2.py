from components.helpers.disponibilidade_data import disponibilidade_data

def opcao2(consultaBase, objeto):
    for i in range(0, 5):
        mes = consultaBase['data']['mes'] + i
        ano = consultaBase['data']['ano']
        dia = consultaBase['data']['dia']
        if mes > 12:
            mes = mes - 12
            ano = ano + 1

        novoObjeto = consultaBase.copy()
        novoObjeto['data'] = {'dia': consultaBase['data']['dia'], 'mes': mes, 'ano': ano}
        dataDisponivel = disponibilidade_data(ano, mes, dia, objeto)
        if dataDisponivel != 'ok':
            return dataDisponivel
        objeto.append(novoObjeto)

    return objeto