from datetime import datetime
from components.helpers.verificacao_HoraeData import comparar_horario

#8-12 / 14-20

def  marcarAutomaticamente():
    diaAtual = datetime.now().day
    mesAtual = datetime.now().month
    anoAtual = datetime.now().year

    dia = diaAtual
    mes = mesAtual
    ano = anoAtual

    hora = [8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8]
    minuto = [0, 30, 0, 30, 0, 30, 0, 30, 0, 30, 0 ,30, 0, 30, 0, 30, 0, 30, 0, 30, 0, 30,0, 30]

    i = 0

    while True:
        
        for i in range(24):
            horario = []
            minutos = []
            horario.append(hora[i])
            minutos.append(minuto[i])
            if comparar_horario(horario, minutos, dia, mes, ano) == True:
                return  dia, mes, ano, hora[i], minuto[i]
        i = 0
        
        dia += 1

        if mes == 2:
            if ano % 4 == 0:
                if dia > 29:
                    dia = 1
                    mes += 1
            else:
                if dia > 28:
                    dia = 1
                    mes += 1

        elif mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
            if dia > 31:
                dia = 1
                mes += 1

        elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
            if dia > 30:
                dia = 1
                mes += 1

        if mes > 12:
            mes -= 12
            ano += 1