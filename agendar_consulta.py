import os
import json
from components.opcao_1 import opcao1
from components.opcao_2 import opcao2
from components.nova_consulta import nova_consulta

def marcarConsulta():
    print('\nBem vindo ao Sistema de Alocação de Consultas\nMarque suas sessões de terapia contra problemas na pele\n')
    consulta = nova_consulta()

    diretorio = './data/'
    caminho_arquivo = f'{diretorio}consultas.json'

    if not os.path.isdir(diretorio):
        os.makedirs(diretorio) # se o dir não existir, ele cria o dir

    if not os.path.isfile(caminho_arquivo):
        dados_iniciais = []
        with open(caminho_arquivo, 'w') as arquivo:
            json.dump(dados_iniciais, arquivo) # se não houver um arquivo, cria o arquivo json com um array vazio

    with open('./data/consultas.json', 'r') as arquivo:
        objeto_python = json.load(arquivo)

    #'\nEscolha o problemaque você tem:\n1 para Aftas\n2 para hipersensiblidade\n3 para lesões\n4 para pós-cirúrgia\n5 para nevralgia\n6 para consulta\n'
    opcao = int(input('\nEscolha o método de seu tratamento:\n1 para a opção de uma sessão por semana - (5 semanas)\n2 para a opção de uma sessão por mês - (5 meses)\n'))
    while True:
        if opcao != 1 and opcao != 2:
            opcao = int(input(
                    '\nEscolha o método de seu tratamento:\n1 para a opção de uma sessão por semana - (5 semanas)\n2 para a opção de uma sessão por mês - (5 meses)\n'))
        else:
            break

    if opcao == 1:
        obj = opcao1(consultaBase=consulta.json(), objeto=objeto_python)

        if type(obj) == str:
            print(f'Data indisponível! Tente novamente com outra data.\nMotivo: {obj}')
            return False
        else:
            objeto_python = obj

    elif opcao == 2:
        obj = opcao2(consultaBase=consulta.json(), objeto=objeto_python)
        if type(obj) == str:
            print(f'Data indisponível! Tente novamente com outra data.\nMotivo: {obj}')
            return False
        else:
            objeto_python = obj

    with open('./data/consultas.json', 'w') as arquivo:
        json.dump(objeto_python, arquivo)

    print('\nConsultas marcadas com sucesso!')
    return True


marcarConsulta()