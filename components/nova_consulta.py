from datetime import datetime

class Data:
    def __init__(self, dia, mes, ano):
        self.dia = dia
        self.mes = mes
        self.ano = ano

    @property
    def data(self):
        return f'{self.dia}/{self.mes}/{self.ano}'

    def json(self):
        return dict(dia=self.dia, mes=self.mes, ano=self.ano)


class Consulta:
    def __init__(self, nome, cpf, data):
        self.nome = nome
        self.cpf = cpf
        self.data = data

    def json(self):
        return dict(nome=self.nome, cpf=self.cpf, data=self.data.json())

    @classmethod
    def parse(cls, dados):
        dados_data = dados.pop('data')
        data = Data(**dados_data)
        dados['data'] = data
        return cls(**dados)

def diaPassou():
    ano = int(input('Diga o ano para sua consulta: '))
    while True:
        if ano < datetime.now().year:
            print('Ano inválido!')
            ano = int(input('Diga o ano para sua consulta: '))
        else:
            break


    mes = int(input('Diga o mês para sua consulta: '))
    while True:
        if ano == datetime.now().year and mes < datetime.now().month:
            print('Mês inválido!')
            mes = int(input('Diga o mês para sua consulta: '))
        else:
            break


    dia = int(input('Diga o dia para sua consulta: '))
    while True:
        if ano == datetime.now().year and mes == datetime.now().month and dia < datetime.now().day:
            print('Dia inválido!')
            mes = int(input('Diga o dia para sua consulta: '))
        else:
            break

    return ano, mes, dia

def checkValidName(nome):
    permitidas = 'ABCDEFGHIJKLMNOPQRSTUVXWYZabcdefghijklmnopqrstuvxwyzáãçéêíóõôú '
    if nome[0] != nome[0].upper():
        return False
    for index in range(len(nome)):
        if nome[index] not in permitidas:
            return False
        if nome[index] == ' ':
            if not nome[index+1] or nome[index+1] == " " or nome[index+1] != nome[index+1].upper():
                return False
        if nome[index] != nome[index].lower():
            if index != 0 and nome[index-1] != ' ':
                return False
    return True


def novaData():
    ano, mes, dia = diaPassou()

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

        ano, mes, dia = diaPassou()

    return Data(dia, mes, ano)

def novaConsulta():
    data=novaData()
    print('\nData pré-alocada com sucesso.\n')
    ok=''

    nome=input('Diga o seu nome: ').strip()
    cpf=input('Diga seu CPF: ').replace('-', '').replace('.', '').strip()

    while True:
        if checkValidName(nome) == True and len(cpf) == 11:
            ok=input(
                f'\n\nDados de sua consulta:\nPaciente: {nome}\nCPF {cpf}\nConsulta agendada em: {data.dia}/{data.mes}/{data.ano}\n\nDigite OK para confirmar: ').lower()
            if ok == 'ok':
                break

        print('DADOS INVÁLIDOS\n')
        nome=input('Diga o seu nome: ').strip()
        cpf=input('Diga seu CPF: ').replace('-', '').replace('.', '').strip()


    return Consulta(nome, cpf, data)
