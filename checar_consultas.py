import json
import datetime

with open('./data/reservas.json', 'r') as arquivo:
    # Carrega o conteúdo do arquivo JSON em um objeto Python
    objeto_python = json.load(arquivo)

def obter_data(item):
    dia = item['data']['dia']
    mes = item['data']['mes']
    ano = item['data']['ano']
    return datetime.datetime(ano, mes, dia)

array_filtrado = sorted(objeto_python, key=obter_data)

i = 1
for objeto in array_filtrado:
    print(f"\nConsulta nº {i}:\nPaciente: {objeto['nome']}\nCPF: {objeto['cpf']}\nData da consulta: {objeto['data']['dia']}/{objeto['data']['mes']}/{objeto['data']['ano']}")
    i = i + 1