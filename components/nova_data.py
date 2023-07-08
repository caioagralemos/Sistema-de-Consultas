from components.helpers.dia_passou import dia_passou
from components.classes.data import Data

def nova_data():
    ano, mes, dia = dia_passou()

    while True:
        razao=''
        if mes == 2:
            if ano % 4 == 0:
                if dia <= 29:
                    break
            else:
                if dia <= 28:
                    break

        elif mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
            if dia <= 31:
                break

        elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
            if dia <= 30:
                break

        print('Data Inválida!\n')

        ano, mes, dia = dia_passou()

    return Data(dia, mes, ano)