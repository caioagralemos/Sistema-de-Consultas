import json
import os

def comparar_horario(hora, minuto, dia, mes, ano):
    # Lendo o JSON

    if not os.path.isdir('./data/'):
        return True
    if not os.path.isfile('./data/consultas.json'):
        return True
    with open('C:/Users/leand/OneDrive/Documentos/GitHub/Sistema-de-Consultas/data/consultas.json', 'r') as file:
        json_data = json.load(file)
    for item in json_data:
        data = item["data"]
        hora_json = data["hora"]
        minuto_json = data["minuto"]
        dia_json = data["dia"]
        mes_json = data["mes"]
        ano_json = data["ano"]

        for i in range(len(hora)):
            for j in range(len(hora_json)):
                if hora[i] == hora_json[j] and minuto[i] == minuto_json[j] and dia == dia_json and mes == mes_json and ano == ano_json:
                    print(f"Horário fornecido corresponde a um dos registros:")
                    print(f"Data: {data['dia']}/{data['mes']}/{data['ano']}")
                    print(f"Nome: {item['nome']}")
                    print(f"CPF: {item['cpf']}")
                    return False
    return True

# Solicitando a entrada do usuário
'''dia_usuario = int(input("Insira o dia: "))
mes_usuario = int(input("Insira o mês: "))
ano_usuario = int(input("Insira o ano: "))
hora_usuario = int(input("Insira a hora: "))
minuto_usuario = int(input("Insira o minuto: "))

# Comparando com o JSON
comparar_horario(hora_usuario, minuto_usuario, dia_usuario, mes_usuario, ano_usuario)'''
