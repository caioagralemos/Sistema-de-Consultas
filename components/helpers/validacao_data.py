from datetime import datetime

def validacao_data():
    #ano = int(input('Diga o ano para sua consulta: '))
    while True:
        ano = int(input('Diga o ano para sua consulta: '))
        if ano < datetime.now().year:
            print('Ano inválido!')
            #ano = int(input('Diga o ano para sua consulta: '))
        else:
            break

    #mes = int(input('Diga o mês para sua consulta: '))
    while True:
        mes = int(input('Diga o mês para sua consulta: '))
        if ano == datetime.now().year and mes < datetime.now().month:
            print('Mês inválido!')
            #mes = int(input('Diga o mês para sua consulta: '))
        elif mes < 1 or mes > 12:
            print('Mês inválido!')
            #mes = int(input('Diga o mês para sua consulta: '))
        else:
            break
        

    #dia = int(input('Diga o dia para sua consulta: '))
    while True:
        dia = int(input('Diga o dia para sua consulta: '))
        if ano == datetime.now().year and mes == datetime.now().month and dia < datetime.now().day:
            print('Dia inválido!')
            #dia = int(input('Diga o dia para sua consulta: '))
        elif dia < 1 or dia > 31:
            print('Dia inválido!')
            #dia = int(input('Diga o dia para sua consulta: '))
        else:
            break

    return ano, mes, dia