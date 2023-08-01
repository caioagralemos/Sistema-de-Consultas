from components.helpers.verificacao_HoraeData import comparar_horario

def validacao_hora(dia, mes, ano):
    hora = [0]
    minuto = [0]
    while True:
        op = int(input('Diga o período para sua consulta:\n1 para manhã\n2 para tarde\n'))
        if op == 1:
            while True:
                hora[0] = int(input('Diga a hora para sua consulta: '))
                if hora[0] > 5 and hora[0] < 13:
                    break
                else:
                    print('Hora inválida!')
        else:
            while True:
                hora[0] = int(input('Diga a hora para sua consulta: '))
                if hora[0] > 14 and hora[0] < 20:
                    break
                else:
                    print('Hora inválida!')

        while True:
            minuto[0] = int(input('Diga o minuto para sua consulta: '))
            if minuto[0] == 0 or minuto[0] == 30:
                break
            elif minuto[0] >= 0 and minuto[0] <= 59:
                print('Minuto inválido! As consultas podem ser marcadas apenas em intervalos de 30 minutos! Dessa forma escolha um desses valores 0 ou 3.')
            else:
                print('Minuto inválido!')
        
        if comparar_horario(hora, minuto, dia, mes, ano):
            break
        else:
            print('Horário indisponível!\nDigite um outro horário!\n')


    return hora, minuto