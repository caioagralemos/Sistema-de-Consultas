import json

def ler_json(arquivo):
    with open(arquivo, 'r') as file:
        data = json.load(file)
    return data

def comparar_horario(json_data, hora, minuto, dia, mes, ano):
    for item in json_data:
        data = item["data"]
        hora_json = data["hora"]
        minuto_json = data["minuto"]
        dia_json = data["dia"]
        mes_json = data["mes"]
        ano_json = data["ano"]
        if hora == hora_json and minuto == minuto_json and dia == dia_json and mes == mes_json and ano == ano_json:
            print(f"Horário fornecido corresponde a um dos registros:")
            print(f"Data: {data['dia']}/{data['mes']}/{data['ano']}")
            print(f"Nome: {item['nome']}")
            print(f"CPF: {item['cpf']}")
            return
    print("Nenhuma correspondência encontrada para o horário fornecido.")

# Lendo o JSON
dados_json = ler_json('consultas.json')

# Solicitando a entrada do usuário
dia_usuario = int(input("Insira o dia: "))
mes_usuario = int(input("Insira o mês: "))
ano_usuario = int(input("Insira o ano: "))
hora_usuario = int(input("Insira a hora: "))
minuto_usuario = int(input("Insira o minuto: "))

# Comparando com o JSON
comparar_horario(dados_json, hora_usuario, minuto_usuario, dia_usuario, mes_usuario, ano_usuario)
