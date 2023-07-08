import os
import json
import datetime

diretorio = './data/'
caminho_arquivo = f'{diretorio}reservas.json'
dia_de_hoje = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

print(f'\nBem vindo ao Sistema de Alocação de Consultas\nConsulte as sessões marcadas \n')

if not os.path.isdir(diretorio):
    os.makedirs(diretorio)

if not os.path.isfile(caminho_arquivo):
    dados_iniciais = []
    with open(caminho_arquivo, 'w') as arquivo:
        json.dump(dados_iniciais, arquivo)

with open('./data/reservas.json', 'r') as arquivo:
    # Carrega o conteúdo do arquivo JSON em um objeto Python
    objeto_python = json.load(arquivo)


def obter_data(item):
    dia = item['data']['dia']
    mes = item['data']['mes']
    ano = item['data']['ano']
    return datetime.datetime(ano, mes, dia)


todas_consultas = sorted(objeto_python, key=obter_data)

choice = input('MENU - Pressione o número da opção desejada:\n1 - todas as consultas\n2 - consultas do dia\n3 - consultas futuras\n4 - consultas passadas\nsua escolha: ')

while True:
    if choice == '1' or choice == '2' or choice == '3' or choice == '4':
        break
    else:
        print('\nOpção Inválida.\n')
        choice = input(
            'MENU - Pressione o número da opção desejada:\n1 - todas as consultas\n2 - consultas do dia\n3 - consultas futuras\n4 - consultas passadas\nsua escolha: ')

if choice == '1':
    i = 1
    if todas_consultas == []:
        print('\nNão há nenhuma consulta em nossos dados.')
    else:
        print('\nTODAS AS CONSULTAS:')
        for objeto in todas_consultas:
            print(
                f"\nConsulta nº {i}:\nPaciente: {objeto['nome']}\nCPF: {objeto['cpf']}\nData da consulta: {objeto['data']['dia']}/{objeto['data']['mes']}/{objeto['data']['ano']}")
            i = i + 1

if choice == '2':
    consultas_do_dia = []
    for consulta in todas_consultas:
        data_consulta = obter_data(consulta)
        if data_consulta == dia_de_hoje:
            consultas_do_dia.append(consulta)
    
    if consultas_do_dia == []:
        print('\nNão há nenhuma consulta marcada para o dia de hoje.')
    else:
        i = 1
        print(f'\nCONSULTAS DO DIA:')
        for objeto in consultas_do_dia:
            print(
                f"\nConsulta nº {i}:\nPaciente: {objeto['nome']}\nCPF: {objeto['cpf']}\nData da consulta: {objeto['data']['dia']}/{objeto['data']['mes']}/{objeto['data']['ano']}")
            i = i + 1

if choice == '3':
    consultas_futuras = []
    for consulta in todas_consultas:
        data_consulta = obter_data(consulta)
        if data_consulta > dia_de_hoje:
            consultas_futuras.append(consulta)
    
    if consultas_futuras == []:
        print('\nNão há nenhuma consulta futura marcada.')
    else:
        i = 1
        print('\nPRÓXIMAS CONSULTAS:')
        for objeto in consultas_futuras:
            print(
                f"\nConsulta nº {i}:\nPaciente: {objeto['nome']}\nCPF: {objeto['cpf']}\nData da consulta: {objeto['data']['dia']}/{objeto['data']['mes']}/{objeto['data']['ano']}")
            i = i + 1

if choice == '4':
    consultas_passadas = []
    for consulta in todas_consultas:
        data_consulta = obter_data(consulta)
        if data_consulta < dia_de_hoje:
            consultas_passadas.append(consulta)
    
    if consultas_passadas == []:
        print('\nNão há nenhuma consulta passada em nossos dados.')
    else:
        i = 1
        print('\nCONSULTAS PASSADAS:')
        for objeto in consultas_passadas:
            print(
                f"\nConsulta nº {i}:\nPaciente: {objeto['nome']}\nCPF: {objeto['cpf']}\nData da consulta: {objeto['data']['dia']}/{objeto['data']['mes']}/{objeto['data']['ano']}")
            i = i + 1