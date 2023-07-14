from components.nova_data import nova_data
from components.classes.consulta import Consulta
from components.helpers.checar_cpf_valido import checar_cpf_valido
from components.helpers.checar_nome_valido import checar_nome_valido

def nova_consulta():
    data=nova_data()
    print('\nData pré-alocada com sucesso.\n')

    nome=input('Diga o seu nome: ').strip() # strip tira os espaços iniciais e finais sobrando
    while True:
        if checar_nome_valido(nome):
            break
        else:
            print('Nome inválido!\n')
            nome=input('Diga o seu nome: ').strip()
            
    cpf=input('Diga seu CPF: ').replace('-', '').replace('.', '').strip()
    while True:
        if checar_cpf_valido(cpf):
            break
        else:
            print('CPF inválido!')
            cpf=input('Diga seu CPF: ').replace('-', '').replace('.', '').strip()

    ok=input(f'\n\nDados de sua consulta:\nPaciente: {nome}\nCPF {cpf}\nConsulta agendada em: {data.dia}/{data.mes}/{data.ano}\n\nDigite OK para confirmar: ').lower()

    if ok == 'ok': 
        return Consulta(nome, cpf, data)
    else:
        print('Agendamento de consulta cancelado.')
        quit()
