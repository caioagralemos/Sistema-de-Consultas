from components.helpers.verificacao_HoraeData import comparar_horario

def validacao_hora(dia, mes, ano):
    while True:
        op = int(input('Diga o período para sua consulta:\n1 para manhã\n2 para tarde\n'))
        if op == 1:
            while True:
                hora = int(input('Diga a hora para sua consulta: '))
                if hora > 5 and hora < 13:
                    break
                else:
                    print('Hora inválida!')
        else:
            while True:
                hora = int(input('Diga a hora para sua consulta: '))
                if hora > 13 and hora < 19:
                    break
                else:
                    print('Hora inválida!')

        while True:
            minuto = int(input('Diga o minuto para sua consulta: '))
            if minuto == 0 or minuto == 10 or minuto == 20 or minuto == 30 or minuto == 40 or minuto == 50:
                break
            elif minuto >= 0 and minuto <= 59:
                print('Minuto inválido! As consultas podem ser marcadas apenas em intervalos de 10 minutos! Dessa forma escolha um desses valores 0, 10, 20, 30, 40 ou 50.')
            else:
                print('Minuto inválido!')
        
        if comparar_horario(hora, minuto, dia, mes, ano):
            break
        else:
            print('Horário indisponível!\nDigite um outro horário!\n')


    return hora, minuto