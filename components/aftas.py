from components.helpers.disponibilidade_data import disponibilidade_data

def aftas(consultaBase, objeto):
    meuDia = consultaBase['data']['dia']
    meuMes = consultaBase['data']['mes']
    meuAno = consultaBase['data']['ano']
    hora = consultaBase['data']['hora']
    minuto = consultaBase['data']['minuto']
    mesesAdicionados = 0
    anosAdicionados = 0
    diasResetados = 0
    mesesResetados = 0
    for diasAdicionados in range(0, 29, 6):
        dia = meuDia + diasAdicionados + diasResetados
        mes = meuMes + mesesAdicionados - mesesResetados
        ano = meuAno + anosAdicionados

        if mes == 2:
            if ano % 4 == 0:
                if dia > 29:
                    mesesAdicionados = mesesAdicionados + 1
                    mes = meuMes + mesesAdicionados - mesesResetados
                    diasResetados = diasResetados - 29
                    dia = meuDia + diasAdicionados + diasResetados
            else:
                if dia > 28:
                    mesesAdicionados = mesesAdicionados + 1
                    mes = meuMes + mesesAdicionados - mesesResetados
                    diasResetados = diasResetados - 28
                    dia = meuDia + diasAdicionados + diasResetados

        elif mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
            if dia > 31:
                mesesAdicionados = mesesAdicionados + 1
                mes = meuMes + mesesAdicionados - mesesResetados
                diasResetados = diasResetados - 31
                dia = meuDia + diasAdicionados + diasResetados

        elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
            if dia > 30:
                mesesAdicionados = mesesAdicionados + 1
                mes = meuMes + mesesAdicionados - mesesResetados
                diasResetados = diasResetados - 31
                dia = meuDia + diasAdicionados + diasResetados

        if mes > 12:
            anosAdicionados = anosAdicionados + 1
            mesesResetados = mesesResetados - 12
            mes = meuMes + mesesAdicionados - mesesResetados
            ano = meuAno + anosAdicionados

        novoObjeto = consultaBase.copy()
        novoObjeto['data'] = {'dia': dia, 'mes': mes, 'ano': ano, 'hora': hora, 'minuto': minuto}

        dataDisponivel = disponibilidade_data(ano, mes, dia, hora, minuto, objeto)

        cont = 0

        while dataDisponivel != 'ok' or cont == 2:
            if mes == 2:
                if ano % 4 == 0:
                    if dia+1 > 29:
                        dia -= 28
                        mes += 1
                elif dia+1 > 28:
                    dia -= 27
                    mes += 1
            elif mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
                if dia+1 > 31:
                    dia -= 30
                    mes += 1
            elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
                if dia > 30:
                    dia -= 29
                    mes += 1
            dataDisponivel = disponibilidade_data(ano, mes, dia, hora, minuto, objeto)
            cont += 1
        
        if cont == 2 and dataDisponivel != 'ok':
            cont = 0
            while dataDisponivel != 'ok' or cont == 2:
                if dia-2 < 1:
                    if mes == 1:
                        dia += 30
                        mes -= 1
                    elif mes == 2:
                        if ano % 4 == 0:
                            dia += 29
                            mes -= 1
                        else:
                            dia += 28
                            mes -= 1
                    elif mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
                        dia += 31
                        mes -= 1
                    elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
                        dia += 30
                        mes -= 1
                dataDisponivel = disponibilidade_data(ano, mes, dia, hora, minuto, objeto)
                cont += 1

        if dataDisponivel != 'ok':
            return dataDisponivel

        objeto.append(novoObjeto)

    return objeto