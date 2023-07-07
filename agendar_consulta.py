import json
import os
from components.nova_consulta import Data, Consulta, novaConsulta
from components.opcao_1 import opcao1
from components.opcao_2 import opcao2
from components.disponibilidade_data import disponibilidade_data


def marcarConsulta():
    print('\nBem vindo ao Sistema de Alocação de Consultas\nMarque suas sessões de terapia contra problemas na pele\n')
    consulta = novaConsulta()

    diretorio = './data/'
    caminho_arquivo = f'{diretorio}reservas.json'

    if not os.path.isdir(diretorio):
        os.makedirs(diretorio)

    if not os.path.isfile(caminho_arquivo):
        dados_iniciais = []
        with open(caminho_arquivo, 'w') as arquivo:
            json.dump(dados_iniciais, arquivo)

    with open('./data/reservas.json', 'r') as arquivo:
        objeto_python = json.load(arquivo)

    dataDisponivel = disponibilidade_data(consulta, objeto_python)

    if dataDisponivel:
        opcao = int(input('\nEscolha o método de seu tratamento:\n1 para a opção de uma sessão por semana - (5 semanas)\n2 para a opção de uma sessão por mês - (5 meses)\n'))
        while True:
            if opcao != 1 and opcao != 2:
                opcao = int(input(
                    '\nEscolha o método de seu tratamento:\n1 para a opção de uma sessão por semana - (5 semanas)\n2 para a opção de uma sessão por mês - (5 meses)\n'))
            else:
                break

        if opcao == 1:
            obj = opcao1(consultaBase=consulta.json(), objeto=objeto_python)
            objeto_python = obj

        elif opcao == 2:
            obj = opcao2(consultaBase=consulta.json(), objeto=objeto_python)
            objeto_python = obj

        with open('./data/reservas.json', 'w') as arquivo:
            json.dump(objeto_python, arquivo)

        print('\nConsultas marcadas com sucesso!')

    else:
        print(
            f'Data indisponível! Tente novamente com outra data.')

marcarConsulta()