from components.helpers.validacao_data import validacao_data
from components.helpers.validacao_hora import validacao_hora
from components.helpers.dataAutomatica import marcarAutomaticamente
from components.classes.data import Data

def nova_data():
    ano, mes, dia = validacao_data()

    while True:
        if mes == 2:
            if ano % 4 == 0:
                if dia <= 29:
                    break
                else:
                    razao = "Dia inválido. Fevereiro tem 29 dias."
            else:
                if dia <= 28:
                    break
                else:
                    razao = "Dia inválido. Fevereiro tem 28 dias."

        elif mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
            if dia <= 31:
                break
            else:
                razao = "Dia inválido. Esse mês tem 31 dias."

        elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
            if dia <= 30:
                break
            else:
                razao = "Dia inválido. Esse mês tem 30 dias."

        print(f'Data Inválida!\n{razao}\n')

        ano, mes, dia = validacao_data()

    hora, minuto = validacao_hora(dia, mes, ano)
    if hora == 'erro':
        dia, mes, ano, hora, minuto = marcarAutomaticamente()
        return Data(dia, mes, ano, hora, minuto)

    