from django.core.exceptions import ValidationError

def checar_cpf_valido(cpf):
    if len(cpf) != 11 or type(cpf) != str:
        return False
    if cpf[0] == cpf[1] and cpf[1] == cpf[2] and cpf[2] == cpf[3] and cpf[3] == cpf[4] and cpf[4] == cpf[5] and cpf[5] == cpf[6] and cpf[6] == cpf[7] and cpf[7] == cpf[8] and cpf[8] == cpf[9] and cpf[9] == cpf[10]:
        return False
    
    cpf_array = []
    calc_verificador_1 = 0
    calc_verificador_2 = 0

    for i in range(0, 9):
        cpf_array.append(int(cpf[i]))
    
    i = 10
    for num in cpf_array:
        calc_verificador_1 = calc_verificador_1 + num*i
        i = i - 1
    primeiro_num_verificador = 11 - (calc_verificador_1 % 11)
    if primeiro_num_verificador >= 10:
        primeiro_num_verificador = 0
    if primeiro_num_verificador != int(cpf[-2]):
        return False
    else:
        cpf_array.append(primeiro_num_verificador)

    i = 11
    for num in cpf_array:
        calc_verificador_2 = calc_verificador_2 + num*i
        i = i - 1
    segundo_num_verificador = 11 - (calc_verificador_2 % 11)
    if segundo_num_verificador >= 10:
        segundo_num_verificador = 0
    if segundo_num_verificador != int(cpf[-1]):
        return False
    
    return True