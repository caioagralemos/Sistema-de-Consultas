from components.helpers.disponibilidade_data import disponibilidade_data

def opcao1(consultaBase, objeto):
    meuDia = consultaBase['data']['dia']
    meuMes = consultaBase['data']['mes']
    meuAno = consultaBase['data']['ano']
    mesesAdicionados = 0
    anosAdicionados = 0
    diasResetados = 0
    mesesResetados = 0
    for diasAdicionados in range(0, 29, 7):
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
        novoObjeto['data'] = {'dia': dia, 'mes': mes, 'ano': ano}

        dataDisponivel = disponibilidade_data(ano, mes, dia, objeto)

        if dataDisponivel != 'ok':
            return dataDisponivel

        objeto.append(novoObjeto)

    return objeto